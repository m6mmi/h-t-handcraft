from django.db.models import Sum

from shopping_cart.models import Cart
from .models import Category


def categories(request):
    return {'categories': Category.objects.all()}


def cart_items_count(request):
    try:
        cart = Cart.objects.get(user_id=request.user, is_active=True)
        count = {'cart_items_count': cart.cartproduct_set.aggregate(total_quantity=Sum('quantity'))['total_quantity']}
        if count['cart_items_count'] is None:
            count = {'cart_items_count': 0}
        return count
    except Cart.DoesNotExist:
        return {'cart_items_count': 0}


