import requests
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class AboutUsView(TemplateView):
    template_name = 'about_us.html'


class TermsAndConditionsView(TemplateView):
    template_name = 'terms_and_conditions.html'


API_KEY = '328b03be55b1e37111ff631fe5786946'


class WeatherView(TemplateView):
    template_name = 'weather.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        city = self.request.GET.get('city', 'Tallinn')

        API_KEY = '328b03be55b1e37111ff631fe5786946'
        URL = 'http://api.openweathermap.org/data/2.5/weather'

        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }

        try:
            response = requests.get(URL, params=params)
            data = response.json()
            if response.status_code == 200:
                weather = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon']
                }
            else:
                weather = None
        except Exception as e:
            weather = None

        context['weather'] = weather
        return context
