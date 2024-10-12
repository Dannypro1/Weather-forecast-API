from datetime import datetime
from lib2to3.fixes.fix_input import context
from django.template import loader
from API.models import Worldcities
from django.http import HttpResponse
from django.shortcuts import render
import geocoder as geocoder
import requests


def go_city(request):
    random_item = Worldcities.objects.all().order_by('?').first()
    city = random_item.city
    location = [random_item.lat, random_item.lng]
    met = get_met(location)
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'city': city,'met': met}, request))

def loc_here(request):
    location = geocoder.ip('me').latlng
    met = get_met(location)
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'met':met},request))


def get_met(location):
    endpoint = "https://api.open-meteo.com/v1/forecast"
    api_request = f"{endpoint}?latitude={location[0]}&longitude={location[1]}&hourly=temperature_2m"
    now = datetime.now()
    hour = now.hour
    meteo_data = requests.get(api_request).json()
    met = meteo_data['hourly']['temperature_2m'][hour]
    return met


# Create your views here.
