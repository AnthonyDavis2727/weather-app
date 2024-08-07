from django.http import HttpRequest
from django.shortcuts import render
import geoip2.database
import requests
import os

def weather(request):

    try:

        # Define variables
        secret_key = os.environ.get('WEATHER_APIKEY')
        default_city = 'London'
        ip = request.META.get('REMOTE_ADDR')
        reader = geoip2.database.Reader('geoip/GeoLite2-City_20240712/GeoLite2-City.mmdb')
        response = reader.city(ip) # Needs to be changed to the variable ip in production
        reader.close()

        # Decide which city information to give to the API
        if request.method == 'POST':
            city = request.POST.get('query')
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={secret_key}'
            weather_info = requests.get(url).json()
            
            if weather_info['cod'] == 200:
                webpage = 'weather/weather.html'

                returned_weather_data = {
                'name': weather_info['name'],
                'weather_condition': weather_info['weather'][0]['main'],
                'temp': int(weather_info['main']['temp']),
                'feels_like_temp': int(weather_info['main']['feels_like']),
                'low': int(weather_info['main']['temp_min']),
                'high': int(weather_info['main']['temp_max']),
                'wind_speed': int(weather_info['wind']['speed']),
                }
                
                context = {'weather': weather, 'returned_weather_data': returned_weather_data}

            else:
                webpage = 'weather/weather_search_error.html'
                context = {'weather': weather}

        elif ip:
            city = response.city.names['en']
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={secret_key}'
            weather_info = requests.get(url).json()
            webpage = 'weather/weather.html'

            returned_weather_data = {
            'name': weather_info['name'],
            'weather_condition': weather_info['weather'][0]['main'],
            'temp': int(weather_info['main']['temp']),
            'feels_like_temp': int(weather_info['main']['feels_like']),
            'low': int(weather_info['main']['temp_min']),
            'high': int(weather_info['main']['temp_max']),
            'wind_speed': int(weather_info['wind']['speed']),
            }

            context = {'weather': weather, 'returned_weather_data': returned_weather_data}

    except (ValueError, geoip2.errors.AddressNotFoundError) as e:
        if request.method == 'POST':
            city = request.POST.get('query')
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={secret_key}'
            weather_info = requests.get(url).json()
            
            if weather_info['cod'] == 200:
                webpage = 'weather/weather.html'

                returned_weather_data = {
                'name': weather_info['name'],
                'weather_condition': weather_info['weather'][0]['main'],
                'temp': int(weather_info['main']['temp']),
                'feels_like_temp': int(weather_info['main']['feels_like']),
                'low': int(weather_info['main']['temp_min']),
                'high': int(weather_info['main']['temp_max']),
                'wind_speed': int(weather_info['wind']['speed']),
                }
                
                context = {'weather': weather, 'returned_weather_data': returned_weather_data}

            else:
                webpage = 'weather/weather_search_error.html'
                context = {'weather': weather}

        else:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={default_city}&units=imperial&appid={secret_key}'
            weather_info = requests.get(url).json()

            if weather_info['cod'] == 200:
                webpage = 'weather/weather.html'

                returned_weather_data = {
                'name': weather_info['name'],
                'weather_condition': weather_info['weather'][0]['main'],
                'temp': int(weather_info['main']['temp']),
                'feels_like_temp': int(weather_info['main']['feels_like']),
                'low': int(weather_info['main']['temp_min']),
                'high': int(weather_info['main']['temp_max']),
                'wind_speed': int(weather_info['wind']['speed']),
                }

                context = {'weather': weather, 'returned_weather_data': returned_weather_data}

            else:
                webpage = 'weather/weather_search_error.html'
                context = {'weather': weather}
    
    return render(request, webpage, context)


def credits(request):
    return render(request, 'weather/credits.html')