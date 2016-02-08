from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import json, urllib
import random


#N2KD_URL = 'http://127.0.0.1:2597/''
SAMPLE_JSON_FILE = '/Users/nated/projects/dwwinst/json_n2k_tiny'

#n2kdResponse = urllib.urlopen(N2KD_URL)
#    data = json.loads(response.read())


data = json.loads(open(SAMPLE_JSON_FILE).read())

#with open(SAMPLE_JSON_FILE) as json_data:
#    data = json.load(json_data)

def index(request):
    template = loader.get_template('basic_inst/index.html')
    return HttpResponse(template.render())

def dataWindSpeed(request):
    windSpeed = data[2]["fields"]["Wind Speed"]
    return JsonResponse({'readout':windSpeed})
