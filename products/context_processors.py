from django.contrib.auth.models import AnonymousUser
from django.db.models import Sum

from shopping_cart.models import Cart
from .models import Category
import requests

def categories(request):
    return {'categories': Category.objects.all()}


def cart_items_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user_id=request.user, is_active=True)
            count = {'cart_items_count': cart.cartproduct_set.aggregate(total_quantity=Sum('quantity'))['total_quantity']}
            if count['cart_items_count'] is None:
                count = {'cart_items_count': 0}
            return count
        except Cart.DoesNotExist:
            return {'cart_items_count': 0}
    else:
        return {'cart_items_count': 0}


def get_weather(request):

    api_key = "328b03be55b1e37111ff631fe5786946"
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