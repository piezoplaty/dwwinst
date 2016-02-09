from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import json, urllib
import random


#N2KD_URL = 'http://127.0.0.1:2597/''
SAMPLE_JSON_FILE = '/Users/nated/projects/dwwinst/json_n2k'

#n2kdResponse = urllib.urlopen(N2KD_URL)
#    data = json.loads(response.read())


#jsonFile = open(SAMPLE_JSON_FILE)

#with open(SAMPLE_JSON_FILE) as json_data:
#    data = json.load(json_data)

def index(request):
    template = loader.get_template('basic_inst/index.html')
    return HttpResponse(template.render())

def dataWind(request):
    WIND_SPEED_PGN = 130306
    data = getJSONInstrumentReadings(WIND_SPEED_PGN)
    #Hack selector TODO remove
    randIndex = random.randint(0,50)
    windSpeed = data[randIndex]["fields"]["Wind Speed"]
    windAngle = data[randIndex]["fields"]["Wind Angle"]
    return JsonResponse({'windSpeed':windSpeed, 'windAngle':windAngle})

def dataBoat(request):
    BOAT_SPEED_SOW_PGN = 128259
    sowReadings = getJSONInstrumentReadings(WIND_SPEED_PGN)
    boatSOW = sowReadings[random.randint(0,50)]["fields"]["Speed Water Referenced"]
    return JsonResponse({'readout':boatSOW})

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