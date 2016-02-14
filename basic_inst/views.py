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
    BOAT_HEADING_PGN = 127250 #fields: Heading
    BOAT_SPEED_COG_SOG_PGN =129026 #COG, SOG

    #Hack selector TODO remove
    randIndex = random.randint(0,50)
    sowReadings = getJSONInstrumentReadings(BOAT_SPEED_SOW_PGN)
    headingReadings = getJSONInstrumentReadings(BOAT_HEADING_PGN)
    cogSogReadings = getJSONInstrumentReadings(BOAT_SPEED_COG_SOG_PGN)

    boatSOW = sowReadings[randIndex]["fields"]["Speed Water Referenced"]
    boatHeading = headingReadings[randIndex]["fields"]["Heading"]
    boatSOG = cogSogReadings[randIndex]["fields"]["SOG"]
    boatCOG = cogSogReadings[randIndex]["fields"]["COG"]
    return JsonResponse({'boatSOW':boatSOW, 'boatHeading':boatHeading, 'boatSOG':boatSOG, 'boatCOG':boatCOG})

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