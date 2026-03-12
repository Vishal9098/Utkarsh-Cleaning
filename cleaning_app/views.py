from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.utils import timezone
from django.views.decorators.http import require_POST
import json

from .models import (
    Category, Service, Cart, CartItem, Order, OrderItem,
    Review, Testimonial, ContactMessage, Coupon, UserProfile
)
from .forms import (
    UserRegistrationForm, UserLoginForm, CheckoutForm,
    ReviewForm, ContactForm, UserProfileForm
)


def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


# ─────────────────────────────────────────
# HOME & MAIN PAGES
# ─────────────────────────────────────────

def home(request):
    categories = Category.objects.filter(is_active=True)
    featured_services = Service.objects.filter(is_featured=True, is_active=True)[:6]
    all_services = Service.objects.filter(is_active=True)[:8]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    context = {
        'categories': categories,
        'featured_services': featured_services,
        'all_services': all_services,
        'testimonials': testimonials,
    }
    return render(request, 'cleaning_app/home.html', context)


def services_list(request):
    services = Service.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)

    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'default')

    if category_slug:
        services = services.filter(category__slug=category_slug)
    if search_query:
        services = services.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    if sort_by == 'price_low':
        services = services.order_by('price')
    elif sort_by == 'price_high':
        services = services.order_by('-price')
    elif sort_by == 'rating':
        services = services.order_by('-rating')

    context = {
        'services': services,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'cleaning_app/services.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    reviews = Review.objects.filter(service=service, is_approved=True)
    related_services = Service.objects.filter(
        category=service.category, is_active=True
    ).exclude(id=service.id)[:4]

    user_reviewed = False
    if request.user.is_authenticated:
        user_reviewed = Review.objects.filter(service=service, user=request.user).exists()

    if request.method == 'POST' and request.user.is_authenticated and not user_reviewed:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.service = service
            review.user = request.user
            review.save()
            # Update service rating
            avg = Review.objects.filter(service=service).aggregate(Avg('rating'))['rating__avg']
            service.rating = round(avg, 1)
            service.review_count = Review.objects.filter(service=service).count()
            service.save()
            messages.success(request, 'Review successfully submitted!')
            return redirect('service_detail', slug=slug)
    else:
        form = ReviewForm()

    context = {
        'service': service,
        'reviews': reviews,
        'related_services': related_services,
        'form': form,
        'user_reviewed': user_reviewed,
    }
    return render(request, 'cleaning_app/service_detail.html', context)


# ─────────────────────────────────────────
# CART
# ─────────────────────────────────────────

def cart_view(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('service').all()
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cleaning_app/cart.html', context)


@require_POST
def add_to_cart(request, service_id):
    service = get_object_or_404(Service, id=service_id, is_active=True)
    cart = get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, service=service)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{service.name} added to cart!',
            'cart_count': cart.get_item_count()
        })
    messages.success(request, f'"{service.name}" cart mein add ho gaya!')
    return redirect('cart')


@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.info(request, 'Item cart se remove ho gaya.')
    return redirect('cart')


@require_POST
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code', '').upper()
        try:
            coupon = Coupon.objects.get(code=code)
            if coupon.is_valid():
                request.session['coupon_code'] = code
                messages.success(request, f'Coupon "{code}" successfully apply ho gaya! {coupon.discount_percent}% discount milega.')
            else:
                messages.error(request, 'Yeh coupon invalid ya expire ho chuka hai.')
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code.')
    return redirect('cart')


# ─────────────────────────────────────────
# CHECKOUT & ORDERS
# ─────────────────────────────────────────

@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('service').all()

    if not cart_items:
        messages.warning(request, 'Cart khaali hai. Pehle koi service add karein.')
        return redirect('services')

    subtotal = cart.get_total()
    discount = 0
    coupon = None

    coupon_code = request.session.get('coupon_code')
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if coupon.is_valid() and subtotal >= coupon.min_order_amount:
                discount = min(subtotal * coupon.discount_percent / 100, coupon.max_discount)
        except Coupon.DoesNotExist:
            pass

    tax = (subtotal - discount) * 18 / 100
    total = subtotal - discount + tax

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                customer_name=form.cleaned_data['customer_name'],
                customer_email=form.cleaned_data['customer_email'],
                customer_phone=form.cleaned_data['customer_phone'],
                address_line1=form.cleaned_data['address_line1'],
                address_line2=form.cleaned_data.get('address_line2', ''),
                city=form.cleaned_data['city'],
                state=form.cleaned_data.get('state', 'Uttar Pradesh'),
                pincode=form.cleaned_data['pincode'],
                subtotal=subtotal,
                discount=discount,
                tax=tax,
                total=total,
                service_date=form.cleaned_data['service_date'],
                service_time=form.cleaned_data['service_time'],
                special_instructions=form.cleaned_data.get('special_instructions', ''),
                payment_method=form.cleaned_data['payment_method'],
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    service=item.service,
                    service_name=item.service.name,
                    price=item.service.get_final_price(),
                    quantity=item.quantity,
                )
            if coupon:
                coupon.used_count += 1
                coupon.save()
                del request.session['coupon_code']

            cart.items.all().delete()
            messages.success(request, f'Order successfully place ho gaya! Order ID: #{str(order.order_id)[:8].upper()}')
            return redirect('order_confirmation', order_id=order.order_id)
    else:
        initial = {}
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                initial = {
                    'customer_name': request.user.get_full_name() or request.user.username,
                    'customer_email': request.user.email,
                    'customer_phone': profile.phone,
                    'address_line1': profile.address,
                    'city': profile.city,
                    'pincode': profile.pincode,
                }
            except:
                initial = {
                    'customer_name': request.user.get_full_name() or request.user.username,
                    'customer_email': request.user.email,
                }
        form = CheckoutForm(initial=initial)

    context = {
        'form': form,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount': discount,
        'tax': round(tax, 2),
        'total': round(total, 2),
        'coupon': coupon,
    }
    return render(request, 'cleaning_app/checkout.html', context)


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'cleaning_app/order_confirmation.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'cleaning_app/my_orders.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'cleaning_app/order_detail.html', {'order': order})


# ─────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Account successfully create ho gaya.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'cleaning_app/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username ya password.')
    else:
        form = UserLoginForm()
    return render(request, 'cleaning_app/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'Successfully logout ho gaye.')
    return redirect('home')


# ─────────────────────────────────────────
# PROFILE
# ─────────────────────────────────────────

@login_required
def profile(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name = request.POST.get('last_name', '')
            request.user.email = request.POST.get('email', '')
            request.user.save()
            messages.success(request, 'Profile update ho gaya!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    orders = Order.objects.filter(user=request.user)[:5]
    context = {'form': form, 'user_profile': user_profile, 'recent_orders': orders}
    return render(request, 'cleaning_app/profile.html', context)


# ─────────────────────────────────────────
# STATIC PAGES
# ─────────────────────────────────────────

def about(request):
    testimonials = Testimonial.objects.filter(is_active=True)
    return render(request, 'cleaning_app/about.html', {'testimonials': testimonials})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message successfully send ho gaya! Hum jald se jald contact karenge.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'cleaning_app/contact.html', {'form': form})
