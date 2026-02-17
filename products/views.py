# products/views.py

from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def product_list(request, category_slug=None):
    category = None
    products = Product.objects.all()
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)