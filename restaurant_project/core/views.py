from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import MenuItem, Order, OrderItem, OrderDetails

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm



from django.core.mail import send_mail
from django.conf import settings


import stripe



def home(request):
    return render(request, 'core/home.html')

def menu(request):
    items = MenuItem.objects.all()
    return render(request, 'core/menu.html', {'items': items})

# ADD TO CART
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart = request.session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, f"{item.name} added to cart.")
    return redirect('view_cart')

# VIEW CART
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for item_id, qty in cart.items():
        item = get_object_or_404(MenuItem, id=int(item_id))
        subtotal = item.price * qty
        cart_items.append({'item': item, 'quantity': qty, 'subtotal': subtotal})
        total += subtotal

    context = {'cart_items': cart_items, 'total': total}
    return render(request, 'core/cart.html', context)

# REMOVE FROM CART
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    cart.pop(str(item_id), None)
    request.session['cart'] = cart
    messages.success(request, "Item removed from cart.")
    return redirect('view_cart')

# DECREASE QUANTITY
def decrease_quantity(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    if cart.get(item_id_str, 0) > 1:
        cart[item_id_str] -= 1
    else:
        cart.pop(item_id_str, None)
    request.session['cart'] = cart
    return redirect('view_cart')

# CLEAR CART
def clear_cart(request):
    request.session['cart'] = {}
    messages.success(request, "Cart cleared.")
    return redirect('view_cart')


# ✅ CHECKOUT + DB Save
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('menu')

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        stripe_token = request.POST.get('stripeToken')

        # Calculate total
        total = sum(
            get_object_or_404(MenuItem, id=int(item_id)).price * quantity
            for item_id, quantity in cart.items()
        )

        try:
            # Create Stripe charge
            charge = stripe.Charge.create(
                amount=int(total * 100),  # Stripe uses paisa (multiply by 100)
                currency='pkr',
                description=f"Order by {request.user.username}",
                source=stripe_token,
            )
        except stripe.error.CardError:
            messages.error(request, "Payment failed. Please check your card.")
            return redirect('checkout')

        # Save order
        order = Order.objects.create(
            customer=request.user,
            payment_method='Card'
        )

        order_details_text = ""
        for item_id, quantity in cart.items():
            item = get_object_or_404(MenuItem, id=int(item_id))
            OrderItem.objects.create(order=order, menu_item=item, quantity=quantity)
            order_details_text += f"{item.name} (x{quantity}) - Rs.{item.price * quantity}\n"

        OrderDetails.objects.create(
            order=order,
            name=name,
            address=address,
            phone=phone,
            total_amount=total
        )

        # Send confirmation email
        message = f"""
Hello {request.user.username},

✅ Your order #{order.id} has been placed successfully!

🧾 Order Summary:
{order_details_text}
Total Paid: Rs.{total}
Payment Method: Card

Thanks for ordering with us!
        """.strip()

        send_mail(
            subject="✅ Order Confirmation",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
            fail_silently=True,
        )

        # Clear cart
        request.session['cart'] = {}
        messages.success(request, "Payment successful and order placed!")
        return redirect('order_confirmation', order_id=order.id)

    total = sum(
        get_object_or_404(MenuItem, id=int(item_id)).price * quantity
        for item_id, quantity in cart.items()
    )

    return render(request, 'core/checkout.html', {
        'total': total,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    })


# USER Authentication

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('menu')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')



@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'core/order_confirmation.html', {'order': order})


#  FOR HISTORY 
@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'core/order_history.html', {'orders': orders})





