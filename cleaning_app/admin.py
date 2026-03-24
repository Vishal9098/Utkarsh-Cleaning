from django.contrib import admin
from .models import Category, Service, ServiceImage, Cart, CartItem, Order, OrderItem, Review, Testimonial, ContactMessage, Coupon, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 2


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discounted_price', 'rating', 'is_featured', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_active', 'discounted_price']
    list_filter = ['category', 'is_featured', 'is_active']
    search_fields = ['name', 'description']
    inlines = [ServiceImageInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['service_name', 'price', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_name', 'customer_phone', 'total', 'status', 'payment_method', 'service_date', 'created_at']
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    list_editable = ['status']
    readonly_fields = ['order_id', 'created_at']
    inlines = [OrderItemInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'service', 'rating', 'is_approved', 'created_at']
    list_editable = ['is_approved']
    list_filter = ['rating', 'is_approved']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'rating', 'is_active']
    list_editable = ['is_active']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'is_read', 'created_at']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'is_active', 'used_count', 'max_uses', 'valid_to']
    list_editable = ['is_active']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'created_at']


admin.site.site_header = "Utkarsh Cleaning Home Services - Admin"
admin.site.site_title = "Utkarsh Cleaning Admin"
admin.site.index_title = "Welcome to Admin Panel"
