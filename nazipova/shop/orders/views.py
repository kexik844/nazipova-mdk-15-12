from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm

def order_create(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    if request.user.is_authenticated:
                        order.user = request.user
                    order.save()
                    
                    for item in cart:
                        product = item['product']
                        if product.stock < item['quantity']:
                            raise ValueError(
                                f'Недостаточно товара {product.name}'
                            )
                        
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            price=item['price'],
                            quantity=item['quantity']
                        )
                        
                        # Уменьшаем количество товара
                        product.stock -= item['quantity']
                        product.save()
                    
                    cart.clear()
                    messages.success(
                        request,
                        f'Заказ #{order.id} успешно оформлен!'
                    )
                    return render(
                        request,
                        'orders/created.html',
                        {'order': order}
                    )
            
            except ValueError as e:
                messages.error(request, str(e))
                return redirect('cart:cart_detail')
    
    else:
        if request.user.is_authenticated:
            form = OrderCreateForm(initial={
                'full_name': request.user.get_full_name(),
            })
        else:
            form = OrderCreateForm()
    
    return render(
        request,
        'orders/create.html',
        {'cart': cart, 'form': form}
    )

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/list.html', {'orders': orders})