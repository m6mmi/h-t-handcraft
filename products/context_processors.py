from django.db.models import Sum

from h_t_handcraft.settings import WEATHER_API_KEY
from shopping_cart.models import Cart
from .models import Category
import requests


def categories(request):
    return {'categories': Category.objects.all()}


def cart_items_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user_id=request.user, is_active=True)
            count = {
                'cart_items_count': cart.cartproduct_set.aggregate(
                    total_quantity=Sum('quantity')
                ).get('total_quantity')
            }
            if not count['cart_items_count']:
                count = {'cart_items_count': 0}
            return count
        except Cart.DoesNotExist or None:
            return {'cart_items_count': 0}
    return {'cart_items_count': 0}


def get_weather(request):
    api_key = WEATHER_API_KEY
    location = "Tallinn"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

    try:
        response = requests.get(weather_url)
        data = response.json()

        if response.status_code == 200:
            weather_data = {
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'city': data['name'],
            }
        else:
            weather_data = {
                'error': 'Could not retrieve weather data'
            }
    except Exception as e:
        weather_data = {
            'error': str(e)
        }

    return {
        'weather_data': weather_data
    }
