# cart/context_processors.py

from cart.models import Cart

def cart_count(request):
    """
    Context processor to make cart count available in all templates
    """
    if request.user.is_authenticated:
        try:
            count = Cart.objects.filter(user=request.user).count()
        except:
            count = 0
    else:
        count = 0
    return {'cart_count': count}