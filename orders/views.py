from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Payment
from cart.models import Cart
import uuid


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items:
        return redirect('cart_detail')

    if request.method == 'POST':
        total_amount = sum(item.subtotal for item in cart_items)

        # Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address_line1=request.POST.get('address_line1'),
            address_line2=request.POST.get('address_line2', ''),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip_code'),
            country=request.POST.get('country'),
            subtotal=total_amount,
            tax=0,
            shipping_cost=0,
            total_amount=total_amount,
            status='pending',
        )

        # Create Order Items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear Cart
        cart_items.delete()

        # Redirect to payment page
        return redirect('payment', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'total_amount': sum(item.subtotal for item in cart_items),
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Prevent duplicate payment
    if hasattr(order, 'payment'):
        return redirect('payment_success', order_id=order.id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if not payment_method:
            context = {
                'order': order,
                'payment_methods': Payment.PAYMENT_METHOD_CHOICES,
                'error': 'Please select a payment method.'
            }
            return render(request, 'orders/payment.html', context)

        # Create Payment
        Payment.objects.create(
            order=order,
            payment_method=payment_method,
            amount=order.total_amount,
            payment_status='completed',  # simulated success
            transaction_id=f"TXN-{uuid.uuid4().hex[:10].upper()}"
        )

        # Update Order Status
        order.status = 'processing'
        order.save()

        return redirect('payment_success', order_id=order.id)

    context = {
        'order': order,
        'payment_methods': Payment.PAYMENT_METHOD_CHOICES,
    }
    return render(request, 'orders/payment.html', context)


@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/payment_success.html', {'order': order})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})
