# 🧹 Utkarsh Cleaning Home Services
## Full-Featured Django E-Commerce Website

---

## 📦 Features

### Customer Features
- ✅ Beautiful homepage with hero section, services, testimonials
- ✅ Service listing with search, filter, sort
- ✅ Service detail with reviews & ratings
- ✅ Shopping cart (session + user based)
- ✅ Coupon code system
- ✅ Checkout with address, scheduling, payment method selection
- ✅ Order confirmation & tracking
- ✅ User registration / login / profile
- ✅ Order history & detail view

### Admin Features
- ✅ Django Admin panel
- ✅ Manage categories, services, images
- ✅ Order management with status updates
- ✅ Customer reviews moderation
- ✅ Testimonials management
- ✅ Coupon code management
- ✅ Contact messages inbox

---

## 🚀 Setup Instructions

### Step 1: Install Requirements
```bash
pip install -r requirements.txt
```

### Step 2: Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Admin User
```bash
python manage.py createsuperuser
```

### Step 4: Load Sample Data
```bash
python manage.py populate_data
```

### Step 5: Run Server
```bash
python manage.py runserver
```

### Step 6: Open in Browser
- **Website**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 🗂️ Project Structure
```
utkarsh_cleaning/
├── manage.py
├── requirements.txt
├── db.sqlite3 (auto-created)
├── utkarsh_cleaning/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── cleaning_app/
    ├── models.py          # All database models
    ├── views.py           # All views/logic
    ├── urls.py            # URL routing
    ├── forms.py           # All forms
    ├── admin.py           # Admin panel config
    ├── context_processors.py
    ├── management/
    │   └── commands/
    │       └── populate_data.py  # Sample data
    └── templates/
        └── cleaning_app/
            ├── base.html
            ├── home.html
            ├── services.html
            ├── service_detail.html
            ├── cart.html
            ├── checkout.html
            ├── order_confirmation.html
            ├── my_orders.html
            ├── order_detail.html
            ├── login.html
            ├── register.html
            ├── profile.html
            ├── about.html
            └── contact.html
```

---

## 🎨 Tech Stack
- **Backend**: Django 4.2
- **Database**: SQLite (can be changed to PostgreSQL)
- **Frontend**: HTML5, CSS3, Vanilla JS
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Poppins + Playfair Display)

---

## 💡 Coupon Codes (Sample)
- `UTKARSH20` → 20% off (max ₹500)
- `PEHLA10` → 10% off (first order)

---

## 📞 Contact
Utkarsh Cleaning Home Services
Lucknow, Uttar Pradesh
Phone: +91 98765 43210
