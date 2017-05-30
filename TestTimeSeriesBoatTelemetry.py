import unittest
import datetime
from TimeSeriesBoatTelemetry import TimeSeriesBoatTelemetry, BoatTelemetryMetric

SAMPLE_JSON_FILE = './json_n2k'

class TestTimeSeriesBoatTelemetry(unittest.TestCase):
    MPS_TO_KTS_FACTOR = 1.944
    WIND_SPEED_N2K_56_SEC = '{"timestamp":"2016-02-08T03:49:56.736Z","prio":2,"src":3,"dst":255,"pgn":130306,"description":"Wind Data","fields":{"SID":80,"Wind Speed":1.85,"Wind Angle":104.7,"Reference":"Apparent"}}'
    WIND_SPEED_GUST_N2K_56_SEC = '{"timestamp":"2016-02-08T03:49:56.936Z","prio":2,"src":3,"dst":255,"pgn":130306,"description":"Wind Data","fields":{"SID":80,"Wind Speed":5.85,"Wind Angle":104.7,"Reference":"Apparent"}}'
    WIND_SPEED_N2K_57_SEC = '{"timestamp":"2016-02-08T03:49:57.736Z","prio":2,"src":3,"dst":255,"pgn":130306,"description":"Wind Data","fields":{"SID":80,"Wind Speed":2.31,"Wind Angle":90.5,"Reference":"Apparent"}}'
    BOAT_SOW_N2K_56_SEC = '{"timestamp":"2016-02-08T03:49:56.983Z","prio":2,"src":36,"dst":255,"pgn":128259,"description":"Speed","fields":{"SID":209,"Speed Water Referenced":6.50}}'
    BOAT_SOW_N2K_57_SEC = '{"timestamp":"2016-02-08T03:49:57.983Z","prio":2,"src":36,"dst":255,"pgn":128259,"description":"Speed","fields":{"SID":209,"Speed Water Referenced":7.70}}'
    BOAT_HEADING_53_SEC = '{"timestamp":"2016-02-08T03:49:53.903Z","prio":2,"src":35,"dst":255,"pgn":127250,"description":"Vessel Heading","fields":{"SID":192,"Heading":157.2,"Deviation":0.0,"Reference":"Magnetic"}}'
    BOAT_COG_SOG_53_SEC = '{"timestamp":"2016-02-08T03:49:53.904Z","prio":2,"src":37,"dst":255,"pgn":129026,"description":"COG & SOG, Rapid Update","fields":{"SID":142,"COG Reference":"True","COG":216.9,"SOG":6.47}}'
    BOAT_PITCH_ROLL_53_SEC = '{"timestamp":"2016-02-08T03:49:53.904Z","prio":3,"src":35,"dst":255,"pgn":127257,"description":"Attitude","fields":{"SID":205,"Pitch":0.4,"Roll":0.2}}'
    BOAT_LAT_LONG_53_SEC = '{"timestamp":"2016-02-08T03:49:53.904Z","prio":3,"src":37,"dst":255,"pgn":129029,"description":"GNSS Position Data","fields":{"SID":143,"Date":"2016.02.08", "Time": "03:49:41","Latitude":47.6478166,"Longitude":-122.3449133,"GNSS type":"GPS+SBAS/WAAS","Method":"DGNSS fix","Integrity":"No integrity checking","Number of SVs":10,"HDOP":0.90,"PDOP":1.70,"Geoidal Separation":-0.01,"Reference Station ID":7}}'

    def test_getCurrentSecondWithNoTelemetry(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        self.assertEqual(None, tsBoatTelem.getCurrentSecond().WindSpeed)
        self.assertEqual(None, tsBoatTelem.getCurrentSecond().WindAngle)
        self.assertEqual(None, tsBoatTelem.getCurrentSecond().SOW)
        self.assertEqual(None, tsBoatTelem.getCurrentSecond().SOG)
        self.assertEqual(None, tsBoatTelem.getCurrentSecond().Heading)

    def test_setGetWindSpeed(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(self.WIND_SPEED_N2K_56_SEC)
        self.assertEqual(1.85 * self.MPS_TO_KTS_FACTOR, tsBoatTelem.getCurrentSecond().WindSpeed)

    def test_setGetLatLong(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(self.BOAT_LAT_LONG_53_SEC)
        self.assertEqual(47.6478166, tsBoatTelem.getCurrentSecond().Latitude)
        self.assertEqual(-122.3449133, tsBoatTelem.getCurrentSecond().Longitude)


    def test_setMultipleWindSpeeds(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(self.WIND_SPEED_N2K_56_SEC)
        tsBoatTelem.processLogLine(self.WIND_SPEED_N2K_56_SEC)
        tsBoatTelem.processLogLine(self.WIND_SPEED_N2K_56_SEC)
        tsBoatTelem.processLogLine(self.WIND_SPEED_N2K_56_SEC)
        tsBoatTelem.processLogLine(self.WIND_SPEED_N2K_56_SEC)
        tsBoatTelem.processLogLine(self.WIND_SPEED_N2K_56_SEC)
        tsBoatTelem.processLogLine(self.WIND_SPEED_N2K_56_SEC)
        tsBoatTelem.processLogLine(self.WIND_SPEED_GUST_N2K_56_SEC)
        self.assertEqual(round(2.35 * self.MPS_TO_KTS_FACTOR, 4), round(tsBoatTelem.getCurrentSecond().WindSpeed, 4))
        self.assertEqual(104.7, round(tsBoatTelem.getCurrentSecond().WindAngle, 1))

    def test_setMultipleBoatSpeed(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(self.BOAT_SOW_N2K_56_SEC)
        tsBoatTelem.processLogLine(self.BOAT_SOW_N2K_56_SEC)
        tsBoatTelem.processLogLine(self.BOAT_SOW_N2K_56_SEC)
        tsBoatTelem.processLogLine(self.BOAT_SOW_N2K_56_SEC)
        self.assertEqual(6.50 * tsBoatTelem.BOAT_SPEED_SOW_FACTOR, tsBoatTelem.getCurrentSecond().SOW)

    def test_invalidJson(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine("Not Real JSON")
        tsBoatTelem.processLogLine(self.WIND_SPEED_N2K_56_SEC)
        self.assertEqual(1.85 * self.MPS_TO_KTS_FACTOR, tsBoatTelem.getCurrentSecond().WindSpeed)

    def test_getAll(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(self.WIND_SPEED_N2K_56_SEC)
        tsBoatTelem.processLogLine(self.BOAT_SOW_N2K_56_SEC)
        #self.assertEqual(1.85, tsBoatTelem.getCurrentSecond().WindSpeed)
        #self.assertEqual(6.50, tsBoatTelem.getCurrentSecond().SOW)

    def test_getBoatTelemetryMetrics(self):
        currentTime = datetime.datetime.now()
        seconds = datetime.timedelta(seconds = 1)
        boatMetrics = BoatTelemetryMetric(currentTime, seconds)
        self.assertEqual(seconds, boatMetrics.Period)
        self.assertEqual(currentTime, boatMetrics.StartTime)
        #self.assertEqual(None, boatMetrics.SOW.Avg)

    def test_setMostRecentDate(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        self.assertEqual(None, tsBoatTelem.mostRecentLogTime)
        tsBoatTelem.processLogLine(self.WIND_SPEED_N2K_56_SEC)
        self.assertEqual(datetime.datetime(2016, 2, 8, 3, 49, 56), tsBoatTelem.mostRecentLogTime)
        tsBoatTelem.processLogLine(self.WIND_SPEED_N2K_57_SEC)
        self.assertEqual(datetime.datetime(2016, 2, 8, 3, 49, 57), tsBoatTelem.mostRecentLogTime)

    def test_getHeadingData(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(self.BOAT_HEADING_53_SEC)
        self.assertEqual(157.2, tsBoatTelem.getCurrentSecond().Heading)

    def test_getSOG(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(self.BOAT_COG_SOG_53_SEC)
        self.assertEqual(6.47 * self.MPS_TO_KTS_FACTOR, tsBoatTelem.getCurrentSecond().SOG)

    def test_getLoadCell(self):
        LOAD_CELL_DATA = '{"src": 99, "description": "Load Cell", "prio": 3, "pgn": 999001, "timestamp": "117-4-2T10:45:32", "dst": 255, "fields": {"LoadCell": "1"}}'
        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(LOAD_CELL_DATA)
        self.assertEqual(1, tsBoatTelem.getCurrentSecond().LoadCell)

    def test_getCOG(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(self.BOAT_COG_SOG_53_SEC)
        self.assertEqual(216.9, tsBoatTelem.getCurrentSecond().COG)

    def test_getTime(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(self.BOAT_COG_SOG_53_SEC)
        self.assertEqual(datetime.datetime(2016,2,8,3,49,53), tsBoatTelem.getCurrentSecond().Time)

    def test_getPitchAndRoll(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(self.BOAT_PITCH_ROLL_53_SEC)
        self.assertEqual(0.4, tsBoatTelem.getCurrentSecond().Pitch)
        self.assertEqual(0.2, tsBoatTelem.getCurrentSecond().Roll)

    def test_loadSampleN2kFile(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        with open(SAMPLE_JSON_FILE, 'rU') as n2kFile:
            for line in n2kFile:
                tsBoatTelem.processLogLine(line)
        tsBoatTelem.printTelemetry()
        self.assertEqual(37, len(tsBoatTelem.TSMetrics))

    def test_loadSampleN2kFileGetAllBoatTelem(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        with open(SAMPLE_JSON_FILE, 'rU') as n2kFile:
            for line in n2kFile:
                tsBoatTelem.processLogLine(line)

        bt = tsBoatTelem.metricsReadAll()
        self.assertEqual(37, len(bt))

    def test_metricReadLine(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(self.WIND_SPEED_N2K_56_SEC)
        tsBoatTelem.processLogLine(self.WIND_SPEED_N2K_57_SEC)
        self.assertEqual(1.85 * self.MPS_TO_KTS_FACTOR, tsBoatTelem.metricsReadline().WindSpeed)
        self.assertEqual(2.31 * self.MPS_TO_KTS_FACTOR, tsBoatTelem.metricsReadline().WindSpeed)
        self.assertEqual(1.85 * self.MPS_TO_KTS_FACTOR, tsBoatTelem.metricsReadline().WindSpeed)

    def test_metricReadLast(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(self.WIND_SPEED_N2K_56_SEC)
        tsBoatTelem.processLogLine(self.WIND_SPEED_N2K_57_SEC)
        self.assertEqual(1.85 * self.MPS_TO_KTS_FACTOR, tsBoatTelem.metricsReadLast().WindSpeed)
        self.assertEqual(1.85 * self.MPS_TO_KTS_FACTOR, tsBoatTelem.metricsReadLast().WindSpeed)


    def test_derriveCurrentDataPortCurrent(self):
        logLineCogSog = '{"timestamp":"2016-02-08T03:49:57.904Z","prio":2,"src":37,"dst":255,"pgn":129026,"description":"COG & SOG, Rapid Update","fields":{"SID":142,"COG Reference":"True","COG":255,"SOG":4.76}}'
        logLineSow = '{"timestamp":"2016-02-08T03:49:57.983Z","prio":2,"src":36,"dst":255,"pgn":128259,"description":"Speed","fields":{"SID":209,"Speed Water Referenced":6.5}}'
        logLineHeading = '{"timestamp":"2016-02-08T03:49:57.903Z","prio":2,"src":35,"dst":255,"pgn":127250,"description":"Vessel Heading","fields":{"SID":192,"Heading":195,"Deviation":0.0,"Reference":"Magnetic"}}'
        nextSecondData = '{"timestamp":"2016-02-08T03:49:58.903Z","prio":2,"src":35,"dst":255,"pgn":127250,"description":"Vessel Heading","fields":{"SID":192,"Heading":195,"Deviation":0.0,"Reference":"Magnetic"}}'

        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(logLineCogSog)
        tsBoatTelem.processLogLine(logLineSow)
        tsBoatTelem.processLogLine(logLineHeading)
        tsBoatTelem.processLogLine(nextSecondData)
        self.assertEqual(315.58230049447343, tsBoatTelem.metricsReadLast().WaterCurrentAngle)
        self.assertEqual(11.45006015851445, tsBoatTelem.metricsReadLast().WaterCurrentSpeed)

    def test_derriveCurrentDataStarboardCurrent(self):
        logLineCogSog = '{"timestamp":"2016-02-08T03:49:57.904Z","prio":2,"src":37,"dst":255,"pgn":129026,"description":"COG & SOG, Rapid Update","fields":{"SID":142,"COG Reference":"True","COG":315,"SOG":4.76}}'
        logLineSow = '{"timestamp":"2016-02-08T03:49:57.983Z","prio":2,"src":36,"dst":255,"pgn":128259,"description":"Speed","fields":{"SID":209,"Speed Water Referenced":6.5}}'
        logLineHeading = '{"timestamp":"2016-02-08T03:49:57.903Z","prio":2,"src":35,"dst":255,"pgn":127250,"description":"Vessel Heading","fields":{"SID":192,"Heading":15,"Deviation":0.0,"Reference":"Magnetic"}}'
        nextSecondData = '{"timestamp":"2016-02-08T03:49:58.903Z","prio":2,"src":35,"dst":255,"pgn":127250,"description":"Vessel Heading","fields":{"SID":192,"Heading":16,"Deviation":0.0,"Reference":"Magnetic"}}'

        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(logLineCogSog)
        tsBoatTelem.processLogLine(logLineSow)
        tsBoatTelem.processLogLine(logLineHeading)
        tsBoatTelem.processLogLine(nextSecondData)
        self.assertEqual(44.41769950552658, tsBoatTelem.metricsReadLast().WaterCurrentAngle)
        self.assertEqual(11.450060158514452, tsBoatTelem.metricsReadLast().WaterCurrentSpeed)

    def test_derriveCurrentDataZeroSow(self):
        logLineCogSog = '{"timestamp":"2016-02-08T03:49:57.904Z","prio":2,"src":37,"dst":255,"pgn":129026,"description":"COG & SOG, Rapid Update","fields":{"SID":142,"COG Reference":"True","COG":60,"SOG":4.76}}'
        logLineSow = '{"timestamp":"2016-02-08T03:49:57.983Z","prio":2,"src":36,"dst":255,"pgn":128259,"description":"Speed","fields":{"SID":209,"Speed Water Referenced":0}}'
        logLineHeading = '{"timestamp":"2016-02-08T03:49:57.903Z","prio":2,"src":35,"dst":255,"pgn":127250,"description":"Vessel Heading","fields":{"SID":192,"Heading":0,"Deviation":0.0,"Reference":"Magnetic"}}'
        nextSecondData = '{"timestamp":"2016-02-08T03:49:58.903Z","prio":2,"src":35,"dst":255,"pgn":127250,"description":"Vessel Heading","fields":{"SID":192,"Heading":1,"Deviation":0.0,"Reference":"Magnetic"}}'

        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(logLineCogSog)
        tsBoatTelem.processLogLine(logLineSow)
        tsBoatTelem.processLogLine(logLineHeading)
        tsBoatTelem.processLogLine(nextSecondData)
        self.assertEqual(240, tsBoatTelem.metricsReadLast().WaterCurrentAngle)
        self.assertEqual(4.76 * self.MPS_TO_KTS_FACTOR, tsBoatTelem.metricsReadLast().WaterCurrentSpeed)

    def test_ZeroCurrent(self):
        tsBoatTelem = TimeSeriesBoatTelemetry()
        SOG = str(6 / tsBoatTelem.BOAT_SPEED_SOG_FACTOR)
        SOW = str(6 / tsBoatTelem.BOAT_SPEED_SOW_FACTOR)
        logLineCogSog = '{"timestamp":"2016-02-08T03:49:57.904Z","prio":2,"src":37,"dst":255,"pgn":129026,"description":"COG & SOG, Rapid Update","fields":{"SID":142,"COG Reference":"True","COG":60,"SOG":' + SOG + '6}}'
        logLineSow = '{"timestamp":"2016-02-08T03:49:57.983Z","prio":2,"src":36,"dst":255,"pgn":128259,"description":"Speed","fields":{"SID":209,"Speed Water Referenced":' + SOW + '}}'
        logLineHeading = '{"timestamp":"2016-02-08T03:49:57.903Z","prio":2,"src":35,"dst":255,"pgn":127250,"description":"Vessel Heading","fields":{"SID":192,"Heading":60,"Deviation":0.0,"Reference":"Magnetic"}}'
        nextSecondData = '{"timestamp":"2016-02-08T03:49:58.903Z","prio":2,"src":35,"dst":255,"pgn":127250,"description":"Vessel Heading","fields":{"SID":192,"Heading":60,"Deviation":0.0,"Reference":"Magnetic"}}'

        tsBoatTelem.processLogLine(logLineCogSog)
        tsBoatTelem.processLogLine(logLineSow)
        tsBoatTelem.processLogLine(logLineHeading)
        tsBoatTelem.processLogLine(nextSecondData)
        self.assertEqual(0, tsBoatTelem.metricsReadLast().WaterCurrentAngle)
        self.assertEqual(0, tsBoatTelem.metricsReadLast().WaterCurrentSpeed)

    def test_OutOfOrderNMEAMessages(self):

        secondOne = '{"timestamp":"2016-02-08T03:49:50.903Z","prio":2,"src":35,"dst":255,"pgn":127250,"description":"Vessel Heading","fields":{"SID":192,"Heading":1,"Deviation":0.0,"Reference":"Magnetic"}}'
        secondTwo = '{"timestamp":"2016-02-08T03:49:51.903Z","prio":2,"src":35,"dst":255,"pgn":127250,"description":"Vessel Heading","fields":{"SID":192,"Heading":2,"Deviation":0.0,"Reference":"Magnetic"}}'
        secondThree = '{"timestamp":"2016-02-08T03:49:52.903Z","prio":2,"src":35,"dst":255,"pgn":127250,"description":"Vessel Heading","fields":{"SID":192,"Heading":3,"Deviation":0.0,"Reference":"Magnetic"}}'

        tsBoatTelem = TimeSeriesBoatTelemetry()
        tsBoatTelem.processLogLine(secondOne)
        tsBoatTelem.processLogLine(secondThree)
        self.assertEqual(1, tsBoatTelem.metricsReadLast().Heading)
        tsBoatTelem.processLogLine(secondTwo)
        self.assertEqual(2, tsBoatTelem.metricsReadLast().Heading)     

if __name__ == '__main__':
    unittest.main()