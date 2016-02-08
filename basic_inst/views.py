from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

import random

def index(request):
    template = loader.get_template('basic_inst/index.html')
    return HttpResponse(template.render())

def dataWindSpeed(request):
    return JsonResponse({'readout':random.randint(0,9)})    
