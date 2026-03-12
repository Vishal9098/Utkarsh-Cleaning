from django.urls import path
from . import views

urlpatterns = [
    # Main Pages
    path('', views.home, name='home'),
    path('services/', views.services_list, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:service_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/coupon/', views.apply_coupon, name='apply_coupon'),

    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmation/<uuid:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/<uuid:order_id>/', views.order_detail, name='order_detail'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Profile
    path('profile/', views.profile, name='profile'),
]
