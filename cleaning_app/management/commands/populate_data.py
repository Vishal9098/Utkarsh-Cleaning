"""
Run: python manage.py populate_data
"""
from django.core.management.base import BaseCommand
from cleaning_app.models import Category, Service, Testimonial, Coupon
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Populate sample data for Utkarsh Cleaning'

    def handle(self, *args, **kwargs):
        self.stdout.write('Sample data add kar rahe hain...')

        # Categories
        cats = [
            ('Home Cleaning', 'home-cleaning', 'fas fa-home', 'Ghar ki complete cleaning'),
            ('Deep Cleaning', 'deep-cleaning', 'fas fa-soap', 'Professional deep cleaning'),
            ('Kitchen Cleaning', 'kitchen-cleaning', 'fas fa-utensils', 'Kitchen ki thorough cleaning'),
            ('Bathroom Cleaning', 'bathroom-cleaning', 'fas fa-bath', 'Bathroom sanitization'),
            ('Sofa & Carpet', 'sofa-carpet', 'fas fa-couch', 'Sofa aur carpet cleaning'),
            ('Pest Control', 'pest-control', 'fas fa-bug', 'Pest control services'),
        ]
        category_objs = {}
        for name, slug, icon, desc in cats:
            cat, _ = Category.objects.get_or_create(
                slug=slug, defaults={'name': name, 'icon': icon, 'description': desc}
            )
            category_objs[slug] = cat
            self.stdout.write(f'  ✓ Category: {name}')

        # Services
        services = [
            ('Basic Home Cleaning', 'basic-home-cleaning', 'home-cleaning',
             'Ghar ki basic cleaning service', 
             'Hamare experienced cleaners aapke ghar ko saaf karenge. Floor mopping, dusting, aur surfaces cleaning included hai.',
             799, 599, '2', '4.8', 45,
             'Floor mopping, Dusting, Surface cleaning, Kitchen counters, Bathroom basic clean'),
            
            ('Full Home Deep Cleaning', 'full-home-deep-cleaning', 'deep-cleaning',
             'Ghar ki sabse thorough deep cleaning',
             'Har kona aur nook ko professionally clean kiya jaayega. Furniture ke peeche, almirahs ke andar sab.',
             2499, 1799, 'full_day', '4.9', 89,
             'Complete deep cleaning, Inside cabinets, Behind furniture, Window cleaning, Floor scrubbing, Bathroom deep clean, Kitchen deep clean'),
            
            ('Kitchen Deep Clean', 'kitchen-deep-clean', 'kitchen-cleaning',
             'Kitchen ki professional deep cleaning',
             'Stove, chimney, tiles, cabinets sab professionally clean. Grease aur stains ko remove karenge.',
             1299, 999, '3', '4.7', 67,
             'Stove cleaning, Chimney cleaning, Tile scrubbing, Cabinet cleaning, Grease removal, Sink deep clean'),
            
            ('Bathroom Sanitization', 'bathroom-sanitization', 'bathroom-cleaning',
             'Complete bathroom cleaning aur sanitization',
             'Toilet, tiles, basin, shower area complete sanitize. Anti-bacterial products use kiye jaate hain.',
             499, 399, '1', '4.8', 112,
             'Toilet deep clean, Tile scrubbing, Basin cleaning, Floor disinfection, Mirror cleaning, Tap polishing'),
            
            ('Sofa Shampooing', 'sofa-shampooing', 'sofa-carpet',
             'Professional sofa cleaning aur shampooing',
             'Sofa ke kapde ko special shampooing se clean kiya jaata hai. Stains remove, odor eliminate.',
             1499, 1199, '3', '4.6', 34,
             'Foam extraction, Stain removal, Odor elimination, Dry cleaning, Fabric protection'),
            
            ('Pest Control', 'pest-control-service', 'pest-control',
             'Ghar ke keede makode se chutkara',
             'Cockroaches, ants, lizards, mice se chutkara. Safe chemicals jo family ke liye harmless hain.',
             1999, 1499, 'half_day', '4.7', 56,
             'Cockroach treatment, Ant treatment, Lizard repellent, Mouse control, 3 month guarantee'),
            
            ('Move-In/Move-Out Cleaning', 'move-in-out-cleaning', 'deep-cleaning',
             'Naye ghar mein jaane ya purane ghar chhorne par',
             'Complete cleaning jo naye ghar ko welcome state mein laaye ya purane ghar ko spotless chhodin.',
             3499, 2799, 'full_day', '4.9', 23,
             'Complete sanitization, All rooms, Kitchen, Bathrooms, Windows, Balcony, Store room'),
            
            ('Carpet Cleaning', 'carpet-cleaning', 'sofa-carpet',
             'Carpet ki professional steam cleaning',
             'Steam cleaning se carpet ke andar ka dirt aur dust completely remove. Carpet jaise naya ho jaata hai.',
             999, 799, '2', '4.5', 41,
             'Steam cleaning, Stain removal, Deodorizing, Drying, Sanitization'),
        ]

        for name, slug, cat_slug, short_desc, desc, price, disc_price, duration, rating, rev_count, includes in services:
            service, _ = Service.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'category': category_objs[cat_slug],
                    'short_description': short_desc,
                    'description': desc,
                    'price': price,
                    'discounted_price': disc_price,
                    'duration': duration,
                    'rating': rating,
                    'review_count': rev_count,
                    'includes': includes,
                    'is_featured': True if slug in ['basic-home-cleaning', 'full-home-deep-cleaning', 'kitchen-deep-clean', 'bathroom-sanitization'] else False,
                }
            )
            self.stdout.write(f'  ✓ Service: {name}')

        # Testimonials
        testimonials = [
            ('Priya Sharma', 'Lucknow', 'Bahut achhi service! Cleaners samay par aaye aur ghar bilkul chamka diya. Bahut khush hoon.', 5),
            ('Rajesh Kumar', 'Kanpur', 'Deep cleaning ke baad lagha ke ghar naya ho gaya. Kitchen aur bathroom ekdum saaf. Highly recommended!', 5),
            ('Sunita Verma', 'Lucknow', 'Sofa cleaning mein bahut professional the. Purane daag bhi nikal gaye. Price bhi reasonable hai.', 4),
            ('Amit Singh', 'Agra', 'Pest control service bahut effective rahi. 3 mahine se koi keeda nahi dikhha. Bahut achha!', 5),
            ('Neha Gupta', 'Lucknow', 'Move-in cleaning ke liye book kiya tha. Flat ekdum saaf mil gaya. Bahut achhi service hai.', 5),
            ('Vivek Mishra', 'Varanasi', 'Regular home cleaning book karte hain. Staff bahut courteous aur professional hai. 5 star!', 5),
        ]
        for name, location, comment, rating in testimonials:
            Testimonial.objects.get_or_create(
                name=name, defaults={'location': location, 'comment': comment, 'rating': rating}
            )
            self.stdout.write(f'  ✓ Testimonial: {name}')

        # Coupons
        Coupon.objects.get_or_create(
            code='UTKARSH20',
            defaults={
                'discount_percent': 20,
                'max_discount': 500,
                'min_order_amount': 500,
                'valid_to': timezone.now() + timedelta(days=365),
            }
        )
        Coupon.objects.get_or_create(
            code='PEHLA10',
            defaults={
                'discount_percent': 10,
                'max_discount': 200,
                'min_order_amount': 0,
                'valid_to': timezone.now() + timedelta(days=365),
            }
        )
        self.stdout.write('\n✅ Sab data successfully add ho gaya!')
        self.stdout.write('📌 Admin: python manage.py createsuperuser')
        self.stdout.write('🚀 Run: python manage.py runserver')
