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

#N2KD_URL = 'http://127.0.0.1:2597/''
SAMPLE_JSON_FILE = '/Users/nated/projects/dwwinst/json_n2k'

#simple prototype to read from string lines from a TCP socket
tsBoatTelem = TimeSeriesBoatTelemetry()

def transferJsonStreamToTelemetry():
    #Listening Port of CANBOAT n2kd stream
    N2KD_STREAM_PORT = 2598
    #Buffer recv size
    BUFFER_RECV = 2048
    #Polling interval
    POLLING_INTERVAL = .100

    #create an INET, STREAMing socket
    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    #now connect to the web server on port 80
    # - the normal http port
    s.connect(("localhost", N2KD_STREAM_PORT))

    stringBuffer = ''
    while True:
        time.sleep(POLLING_INTERVAL)
        recvBuffer = s.recv(BUFFER_RECV)

        stringBuffer += str(recvBuffer)
        #This seems a bit ditry, how do I know that I'm not going to truncate a n2k message and get a partial line
        stringLines = stringBuffer.split('\n')

        for logLine in stringLines:
            if logLine.endswith("}}"): 
                tsBoatTelem.processLogLine(logLine)
            else:
                stringBuffer = logLine


t = threading.Thread(target=transferJsonStreamToTelemetry)
t.setDaemon(True)
t.start()


with open(SAMPLE_JSON_FILE, 'rU') as n2kFile:
    for line in n2kFile:
        tsBoatTelem.processLogLine(line)


def index(request):
    template = loader.get_template('basic_inst/index.html')
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