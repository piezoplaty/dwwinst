import json
import datetime
import dateutil.parser
from Metric import Metric

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
    def __str__(self):
        return self.Time.isoformat() + ", " + str(self.SOW) + ", " + str(self.Heading) + ", " + str(self.SOG) + ", " + str(self.COG) + ", " + str(self.WindSpeed) + ", " + str(self.WindAngle) + ", " + str(self.Pitch) + ", " + str(self.Roll)
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

class TimeSeriesBoatTelemetry:
    BOAT_SPEED_SOW_PGN = 128259
    BOAT_HEADING_PGN = 127250 #fields: Heading
    BOAT_SPEED_COG_SOG_PGN = 129026 #COG, SOG
    WIND_SPEED_PGN = 130306
    BOAT_PITCH_ROLL = 127257

    def __init__(self):
        self.TSMetrics = dict()
        self.mostRecentLogTime = None
        self.metricsPosition = None
    
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

    #Takes a JSON string as input, parses out interesting boat telemetry
    #Creates metrics for each interesting telemetry
    def processLogLine(self, strLogLine):
        try:
            jsonLogLine = json.loads(strLogLine)
        except:
            print "Processed and invalid json line"
            return
        
        logLineTime = dateutil.parser.parse(jsonLogLine["timestamp"])
        logLineTime = self.roundDownToSecond(logLineTime)
        self.setMostRecentLogTime(logLineTime)
        metrics = self.getMetricEntry(logLineTime)
        
        if jsonLogLine["pgn"] == self.WIND_SPEED_PGN:
            metrics.WindSpeedMetric.addDataPoint(jsonLogLine["fields"]["Wind Speed"])
            metrics.WindAngleMetric.addDataPoint(jsonLogLine["fields"]["Wind Angle"])
        if jsonLogLine["pgn"] == self.BOAT_SPEED_SOW_PGN:
            metrics.SOWMetric.addDataPoint(jsonLogLine["fields"]["Speed Water Referenced"])
        if jsonLogLine["pgn"] == self.BOAT_HEADING_PGN:
            metrics.HeadingMetric.addDataPoint(jsonLogLine["fields"]["Heading"])
        if jsonLogLine["pgn"] == self.BOAT_SPEED_COG_SOG_PGN:
            metrics.SOGMetric.addDataPoint(jsonLogLine["fields"]["SOG"])
            metrics.COGMetric.addDataPoint(jsonLogLine["fields"]["COG"])
        if jsonLogLine["pgn"] == self.BOAT_PITCH_ROLL:
            metrics.PitchMetric.addDataPoint(jsonLogLine["fields"]["Pitch"])
            metrics.RollMetric.addDataPoint(jsonLogLine["fields"]["Roll"])


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
        keylist = self.TSMetrics.keys()
        keylist.sort()
        for key in keylist:
            print self.convertMetricsToSimpleTelemetry(self.TSMetrics[key])

    #iterates through metrics in time sorted order (by key)
    #returns None at the end of the metrics
    #adding additional metrics resumes the process
    def metricsReadline(self):
        if self.metricsPosition is None:
            self.metricsPosition = 0
        else:
            self.metricsPosition += 1

        keylist = self.TSMetrics.keys()
        keylist.sort()

        if len(keylist) == self.metricsPosition:
            self.metricsPosition = 0
        
        return self.convertMetricsToSimpleTelemetry(self.TSMetrics[keylist[self.metricsPosition]])

    #returns BoatTelemetry from -1 second of the mostRecentLog time. 
    #The -1 metrics should be complete because all transducers should have 
    #emitted a log line. Where as the most recent metric will be
    #incomplete, as some n2k transducers only emit metrics every second. 
    def metricsReadLast(self):
        lastLogTime = self.roundDownToSecond(self.mostRecentLogTime - datetime.timedelta(seconds=1))
        print lastLogTime
        #TODO
        #if self.TSMetrics.exists(lastLogTime):
        return self.convertMetricsToSimpleTelemetry(self.TSMetrics[lastLogTime])

    #Returns a list of BoatTelemtry entries, ordered by time
    def metricsReadAll(self):
        keylist = self.TSMetrics.keys()
        keylist.sort()

        bt = list()
        for key in keylist:
            bt.append(self.convertMetricsToSimpleTelemetry(self.TSMetrics[key]))
        return bt
