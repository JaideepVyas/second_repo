# cart/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart
from products.models import Product

@login_required
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.subtotal for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart/cart_detail.html', context)

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart.quantity += 1
        cart.save()
    return redirect('cart_detail')

@login_required
def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, user=request.user, product_id=product_id)
    cart.delete()
    return redirect('cart_detail')

@login_required
def cart_clear(request):
    Cart.objects.filter(user=request.user).delete()
    return redirect('cart_detail')