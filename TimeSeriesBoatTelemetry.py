import json
import datetime
import math
import dateutil.parser
from Metric import Metric

#This is a sorta struct that we pass to external callers.
class BoatTelemetry:
    def __init__(self):
        self.Time = None
        self.SOW = None
        self.Heading = None
        self.SOG = None
        self.COG = None
        self.WindSpeed = None
        self.WindAngle = None
        self.Pitch = None
        self.Roll = None
        self.Latitude = None
        self.Longitude = None
        self.WaterCurrentSpeed = None
        self.WaterCurrentAngle = None
        self.LoadCell = None
    def __str__(self):
        return self.Time.isoformat() + ", " + str(self.SOW) + ", " + str(self.Heading) + ", " + str(self.SOG) + ", " + str(self.COG) + ", " + str(self.WaterCurrentAngle) + ", " + str(self.WaterCurrentSpeed) + str(self.WindSpeed) + ", " + str(self.WindAngle) + ", " + str(self.Pitch) + ", " + str(self.Roll) + ", " + str(self.Latitude) + ", " + str(self.Longitude) + ", " + str(self.LoadCell)
    def __repr__(self):
        return self.__str__()

class BoatTelemetryMetric:
    def __init__(self, startTime, period):
        self.StartTime = startTime
        self.Period = period
        self.SOWMetric = Metric("SOW")
        self.WindSpeedMetric = Metric("Wind Speed")
        self.WindAngleMetric = Metric("Wind Angle")
        self.HeadingMetric = Metric("Heading")
        self.SOGMetric = Metric("SOG")
        self.COGMetric = Metric("COG")
        self.PitchMetric = Metric("Pitch")
        self.RollMetric = Metric("Roll")
        self.LatitudeMetric = Metric("Latitude")
        self.LongitudeMetric = Metric("Longitude")
        self.WaterCurrentSpeed = Metric("Water Current Speed")
        self.WaterCurrentAngle = Metric("Water Current Angle")
        self.LoadCellMetric = Metric("Load Cell")

class TimeSeriesBoatTelemetry:
    BOAT_SPEED_SOW_PGN = 128259
    BOAT_HEADING_PGN = 127250 #fields: Heading
    BOAT_SPEED_COG_SOG_PGN = 129026 #COG, SOG
    WIND_SPEED_PGN = 130306
    BOAT_PITCH_ROLL_PGN = 127257
    BOAT_LAT_LONG_PGN = 129029
    MAGNETIC_VARIATION = 127258
    LOAD_CELL_PGN = 999001
    

    #Scaling Factors - some PGNs values need a scaling factor to line up with the units we want.
    #Stole the factors from here: https://github.com/canboat/canboat/issues/7
    #1.944 converts meters per second to kts. The SOW number must be adjusted specific to the boat install
    #So calibrate the SOW to match COG in times of slack current.
    BOAT_SPEED_SOW_FACTOR = 1.97
    BOAT_SPEED_SOG_FACTOR = 1.944
    WIND_SPEED_FACTOR = 1.944


    def __init__(self):
        self.TSMetrics = dict()
        self.mostRecentLogTime = None
        self.metricsPosition = None
        #Grabs the latest GPS=source decliation value from the wire and stores it
        #The value doesn't change very often, so we don't need a metric for it.
        self.magneticVariation = 0.0
    
    def roundDownToSecond(self, inputDateTime):
        return datetime.datetime(inputDateTime.year, inputDateTime.month, inputDateTime.day, inputDateTime.hour, inputDateTime.minute, inputDateTime.second, 0)

    def setMostRecentLogTime(self, logTime):
        if self.mostRecentLogTime is None:
            self.mostRecentLogTime = logTime
        else:
            self.mostRecentLogTime = max(logTime, self.mostRecentLogTime)
 
    def getMetricEntry(self, key):
        try:
            return self.TSMetrics[key]
        except KeyError as e:
            self.TSMetrics[key] = BoatTelemetryMetric(key, datetime.timedelta(seconds =1))
            return self.TSMetrics[key]

    def isSogPortOfHeading(self, cog, heading):
        diff = cog - heading
        if diff < 0 and diff > -180 or diff > 180:
            return True
        else:
            return False

    #Given -degrees or degress > 360, return the equalinet value between 0 and 360
    def absDegrees(self, origDeg):
        if origDeg < 0:
            return 360 + (origDeg % -360)
        else:
            return (origDeg % 360)

    #Uses a metric set to compute current angle and speed
    #Requires that each of COG, SOG, SOW, and Heading be set, otherwise the current metrics 
    #are not computed and the method does nothing
    def computeWaterCurrentMetrics(self, metrics):
        try:
            #Do nothing if we don't have all the metrics we need in this set.
            if metrics.SOWMetric.N == 0 or metrics.HeadingMetric.N == 0 or metrics.SOGMetric.N == 0 or metrics.COGMetric.N == 0:
                return
            else:
                sow = metrics.SOWMetric.Avg
                heading =metrics.HeadingMetric.Avg
                sog = metrics.SOGMetric.Avg
                cog = metrics.COGMetric.Avg
                cogHeadingDiff =  self.absDegrees(cog - heading)
                cogHeaddiffRadians = (math.pi / 180) * cogHeadingDiff
                currentSpeed = math.sqrt(math.pow(sog, 2) + math.pow(sow,2) - (2 * sow * sog * math.cos(cogHeaddiffRadians)))
                if sow == 0 or currentSpeed == 0: # If sow is 0, then our current a can be computed with cog and heading data
                    vectorCurrentAngle = cog #TODO, need to figure out current angle relantive to the boat
                else:
                    vectorCurrentAngle = math.acos((math.pow(currentSpeed,2) + math.pow(sow,2) - math.pow(sog,2)) / (2 * currentSpeed * sow)) * (180 / math.pi)
                
                if sow == 0:
                    currentAngle = self.absDegrees(cog - 180)
                elif currentSpeed == 0:
                    currentAngle = 0
                elif self.isSogPortOfHeading(cog, heading):
                    currentAngle =  vectorCurrentAngle
                else:
                    currentAngle = 360 - vectorCurrentAngle
                metrics.WaterCurrentAngle.addDataPoint(currentAngle)
                metrics.WaterCurrentSpeed.addDataPoint(currentSpeed)
        except:
            print("Encountered an exception while computing current angles and speed.")
            return

    #Takes a JSON string as input, parses out interesting boat telemetry
    #Creates metrics for each interesting telemetry
    def processLogLine(self, strLogLine):
        try:
            jsonLogLine = json.loads(strLogLine)
        except:
            print("Processed and invalid json line")
            return
        
        logLineTime = dateutil.parser.parse(jsonLogLine["timestamp"])
        logLineTime = self.roundDownToSecond(logLineTime)
        print ("Processing log line for " + str(logLineTime))
        self.setMostRecentLogTime(logLineTime)
        metrics = self.getMetricEntry(logLineTime)
        
        if jsonLogLine["pgn"] == self.WIND_SPEED_PGN:
            metrics.WindSpeedMetric.addDataPoint(float(jsonLogLine["fields"]["Wind Speed"]) * self.WIND_SPEED_FACTOR)
            metrics.WindAngleMetric.addDataPoint(jsonLogLine["fields"]["Wind Angle"])
        if jsonLogLine["pgn"] == self.BOAT_SPEED_SOW_PGN:
            metrics.SOWMetric.addDataPoint(float(jsonLogLine["fields"]["Speed Water Referenced"]) * self.BOAT_SPEED_SOW_FACTOR)
            self.computeWaterCurrentMetrics(metrics)
        if jsonLogLine["pgn"] == self.BOAT_HEADING_PGN:
            trueNorthHeading = float(jsonLogLine["fields"]["Heading"]) + self.magneticVariation
            trueNorthHeading = self.absDegrees(trueNorthHeading)
            metrics.HeadingMetric.addDataPoint(trueNorthHeading)
            self.computeWaterCurrentMetrics(metrics)
        if jsonLogLine["pgn"] == self.BOAT_SPEED_COG_SOG_PGN:
            metrics.SOGMetric.addDataPoint(float(jsonLogLine["fields"]["SOG"]) * self.BOAT_SPEED_SOG_FACTOR)
            metrics.COGMetric.addDataPoint(jsonLogLine["fields"]["COG"])
            self.computeWaterCurrentMetrics(metrics)
        if jsonLogLine["pgn"] == self.BOAT_PITCH_ROLL_PGN:
            metrics.PitchMetric.addDataPoint(jsonLogLine["fields"]["Pitch"])
            metrics.RollMetric.addDataPoint(jsonLogLine["fields"]["Roll"])
        if jsonLogLine["pgn"] == self.BOAT_LAT_LONG_PGN:
            metrics.LatitudeMetric.addDataPoint(jsonLogLine["fields"]["Latitude"])
            metrics.LongitudeMetric.addDataPoint(jsonLogLine["fields"]["Longitude"])
        if jsonLogLine["pgn"] == self.MAGNETIC_VARIATION:
            self.magneticVariation = float(jsonLogLine["fields"]["Variation"])
        if jsonLogLine["pgn"] == self.LOAD_CELL_PGN:
            metrics.LoadCellMetric.addDataPoint(jsonLogLine["fields"]["LoadCell"])


    def convertMetricsToSimpleTelemetry(self, metrics):
        bt = BoatTelemetry()
        bt.Time = metrics.StartTime
        bt.SOW = metrics.SOWMetric.Avg
        bt.WindSpeed = metrics.WindSpeedMetric.Avg
        bt.WindAngle = metrics.WindAngleMetric.Avg
        bt.Heading = metrics.HeadingMetric.Avg
        bt.SOG = metrics.SOGMetric.Avg
        bt.COG = metrics.COGMetric.Avg
        bt.Pitch = metrics.PitchMetric.Avg
        bt.Roll = metrics.RollMetric.Avg
        bt.Latitude = metrics.LatitudeMetric.Avg
        bt.Longitude = metrics.LongitudeMetric.Avg
        bt.WaterCurrentAngle = metrics.WaterCurrentAngle.Avg
        bt.WaterCurrentSpeed = metrics.WaterCurrentSpeed.Avg
        bt.LoadCell = metrics.LoadCellMetric.Avg
        return bt

    def getCurrentSecond(self):
        bt = BoatTelemetry()

        #Make sure we actually have data
        try:
            if self.mostRecentLogTime is None:
                return bt
            else:
                metrics = self.TSMetrics[self.mostRecentLogTime]
        except KeyError as e:
            #No metrics found in the last second
            return bt

        bt = self.convertMetricsToSimpleTelemetry(metrics)
        return bt

    def printTelemetry(self):
        keylist = sorted(self.TSMetrics.keys())

        for key in keylist:
            print(self.convertMetricsToSimpleTelemetry(self.TSMetrics[key]))

    #iterates through metrics in time sorted order (by key)
    #returns None at the end of the metrics
    #adding additional metrics resumes the process
    def metricsReadline(self):
        if self.metricsPosition is None:
            self.metricsPosition = 0
        else:
            self.metricsPosition += 1

        keylist = sorted(self.TSMetrics.keys())
        
        #end of the list, start over
        if len(keylist) == self.metricsPosition:
            self.metricsPosition = 0
        
        return self.convertMetricsToSimpleTelemetry(self.TSMetrics[keylist[self.metricsPosition]])

    #returns BoatTelemetry second to last in time sorted metrics
    #the most current metric is likley incomplete. Note this doesn't 
    #guard against random time metrics
    def metricsReadLast(self):
        keylist = sorted(self.TSMetrics.keys())
        secondToLast = len(keylist) - 2
    
        return self.convertMetricsToSimpleTelemetry(self.TSMetrics[keylist[secondToLast]])

    def metricsGetLastMetrics(self):
        if self.mostRecentLogTime is None:
            return
        lastLogTime = self.roundDownToSecond(self.mostRecentLogTime - datetime.timedelta(seconds=1))
        return self.TSMetrics[lastLogTime]

    #Returns a list of BoatTelemtry entries, ordered by time
    def metricsReadAll(self):
        keylist = sorted(self.TSMetrics.keys())

        bt = list()
        for key in keylist:
            bt.append(self.convertMetricsToSimpleTelemetry(self.TSMetrics[key]))
        return bt
