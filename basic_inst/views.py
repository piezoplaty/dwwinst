from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import json, urllib
import random
from TimeSeriesBoatTelemetry import TimeSeriesBoatTelemetry, BoatTelemetryMetric
import ReadSocket
import threading
import socket
import time



#simple prototype to read from string lines from a TCP socket
tsBoatTelem = TimeSeriesBoatTelemetry()

def readFromSocket(socket, _tsBoatTelem):
    #Buffer recv size
    BUFFER_RECV = 2048
    #Polling interval
    POLLING_INTERVAL = .100
    stringBuffer = ''
    
    while True:
        time.sleep(POLLING_INTERVAL)
        recvBuffer = socket.recv(BUFFER_RECV)

        stringBuffer += str(recvBuffer)
        #This seems a bit dirty, how do I know that I'm not going to truncate a n2k message and get a partial line
        stringLines = stringBuffer.split('\n')

        for logLine in stringLines:
            if logLine.endswith("}}"): 
                tsBoatTelem.processLogLine(logLine)
            else:
                stringBuffer = logLine   

def transferJsonStreamToTelemetry(n2kdPort):
    #create an INET, STREAMing socket
    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

    s.connect(("localhost", n2kdPort))
    readFromSocket(s, tsBoatTelem)

def transferMainMetricTelemetry():
    #Listening Port of CANBOAT n2kd stream
    N2KD_STREAM_PORT = 2598
    transferJsonStreamToTelemetry(N2KD_STREAM_PORT)

def transferBeanLoadCellMetricTelemetry():
    #BeanLoadCell reader port
    N2KD_BEAN_STREAM = 2596
    transferJsonStreamToTelemetry(N2KD_BEAN_STREAM)



mainMetricThread = threading.Thread(target=transferMainMetricTelemetry)
mainMetricThread.setDaemon(True)
mainMetricThread.start()

loadCellMetricThread = threading.Thread(target=transferBeanLoadCellMetricTelemetry)
loadCellMetricThread.setDaemon(True)
loadCellMetricThread.start()

#Directly load an n2k file
#N2KD_URL = 'http://127.0.0.1:2597/''
#SAMPLE_JSON_FILE = '/Users/nated/projects/dwwinst/json_n2k'
#with open(SAMPLE_JSON_FILE, 'rU') as n2kFile:
#    for line in n2kFile:
#        tsBoatTelem.processLogLine(line)


def index(request):
    template = loader.get_template('basic_inst/index.html')
    return HttpResponse(template.render())

def single_inst(request):
    template = loader.get_template('basic_inst/single_inst.html')
    return HttpResponse(template.render())

def view_controllers(request):
    template = loader.get_template('basic_inst/view-controllers.js')
    return HttpResponse(template.render())

def view_jquery(request):
    template = loader.get_template('basic_inst/jquery.min.js')
    return HttpResponse(template.render())

def dataWind(request):
    metrics = tsBoatTelem.metricsReadLast()
    windSpeed = metrics.WindSpeed
    windAngle = metrics.WindAngle

    #TODO Replace with db lookup for AWA
    TARGET_AWA = 30

    return JsonResponse({'windSpeed':windSpeed, 'windAngle':windAngle, 'windTargetAngle': TARGET_AWA})

def dataBoat(request):
    #Hack - replace with db lookup
    TARGET_BOAT_SPEED = 6.5

    metrics = tsBoatTelem.metricsReadLast()
    boatSOW = metrics.SOW
    boatHeading = metrics.Heading
    boatSOG = metrics.SOG
    boatCOG = metrics.COG
    return JsonResponse({'boatSOW':boatSOW, 'boatHeading':boatHeading, 'boatSOG':boatSOG, 'boatCOG':boatCOG, 'boatTargetSpeed': TARGET_BOAT_SPEED})

def dataAll(request):
    metrics = tsBoatTelem.metricsGetLastMetrics()
    jsonMetrics = []

    jsonMetrics.append({"keyName" : "SOW", "displayName" : "SOW", "value" : metrics.SOWMetric.Avg, "targetValue" : None})
    jsonMetrics.append({"keyName" : "SOG", "displayName" : "SOG", "value" : metrics.SOGMetric.Avg, "targetValue" : None})
    jsonMetrics.append({"keyName" : "Heading", "displayName" : "Heading", "value" : metrics.HeadingMetric.Avg, "targetValue" : None})
    jsonMetrics.append({"keyName" : "COG", "displayName" : "COG", "value" : metrics.COGMetric.Avg, "targetValue" : None})
    jsonMetrics.append({"keyName" : "Windspeed", "displayName" : "Wind Speed", "value" : metrics.WindSpeedMetric.Avg, "targetValue" : None})
    jsonMetrics.append({"keyName" : "Windangle", "displayName" : "Wind Angle", "value" : metrics.WindAngleMetric.Avg, "targetValue" : None})
    jsonMetrics.append({"keyName" : "WaterCurrentAngle", "displayName" : "Water Current Angle", "value" : metrics.WaterCurrentAngle.Avg, "targetValue" : None})
    jsonMetrics.append({"keyName" : "WaterCurrentSpeed", "displayName" : "Water Current Speed", "value" : metrics.WaterCurrentSpeed.Avg, "targetValue" : None})
    jsonMetrics.append({"keyName" : "MetricTime", "displayName" : "Metric Time", "value" : metrics.StartTime, "targetValue" : None})
    jsonMetrics.append({"keyName" : "LoadCell", "displayName" : "Load Cell", "value" : metrics.LoadCellMetric.Avg, "targetValue" : None})
    #jsonMetrics.append({"keyName" : "Roll", "displayName" : "Roll", "value" : metrics.RollMetric.Avg, "targetValue" : None})
    #jsonMetrics.append({"keyName" : "Pitch", "displayName" : "Pitch", "value" : metrics.PitchMetric.Avg, "targetValue" : None})
    #jsonMetrics.append({"keyName" : "LatLong", "displayName" : "Lat Long", "value" : str(metrics.LatitudeMetric.Avg) + ", \n" + str(metrics.LongitudeMetric.Avg), "targetValue" : None})

    return JsonResponse(jsonMetrics, safe=False)    

def downloadTelemetryHistory(request):
    responseBody = ''
    for metrics in tsBoatTelem.metricsReadAll():
        responseBody += str(metrics) + '\n'
    response = HttpResponse(responseBody, content_type='application/csv')
    response["Content-Disposition"] = "attachment; filename=boat_telem.csv"
    return response

    #return HttpResponse(tsBoatTelem.metricsReadAll())

#Canboat analyzer and n2kd return well formed JSON lines that contain all sensor data 
#jumbled together. This functions extracts sensor specific using the pgn key
#and adds additional JSON syntax to create a valid JSON map of sensor readings.
def getJSONInstrumentReadings(pgn):
    readings = "["
    firstRun = True
    with open(SAMPLE_JSON_FILE, 'rU') as jsonFile:
        for line in jsonFile:
            if "\"pgn\":" + str(pgn) in line:
                if firstRun:
                    firstRun = False
                else:
                    readings += ",\n"
                readings += line
    readings = readings + "]"
    return json.loads(readings)
