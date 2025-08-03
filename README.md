# 🍽️ Django Restaurant Website

This is a full-stack Django-based restaurant website that allows users to:

- Register/Login and manage their profile
- Browse a dynamic food menu with images
- Add items to cart and view subtotal
- Choose payment method (Cash/Card)
- Complete the checkout process
- View order confirmation and (optionally) history

---

## 🛠️ Features

- ✅ **User Authentication** (Register, Login, Logout)
- ✅ **Dynamic Menu System** (Food items stored in database)
- ✅ **Cart Functionality** (Add, Remove, Decrease Quantity, Clear Cart)
- ✅ **Order Placement** (Form-based checkout with validation)
- ✅ **Payment Method Selection** (Cash or Card)
- ✅ **Session Management** (Cart stored in session)
- ✅ **Admin Panel** for managing menu and orders
- ✅ **Responsive UI** (Custom CSS)

---

## 🔧 Technologies Used

- **Backend**: Python, Django
- **Frontend**: HTML5, CSS3 (custom styles)
- **Database**: SQLite3 (default Django database)
- **Deployment Ready**: Easily deployable on platforms like Heroku, Vercel (with configuration)

---

## 📁 Folder Structure

restaurant_project/
│
├── core/
│ ├── models.py # MenuItem, Order, OrderDetails models
│ ├── views.py # All business logic and cart functionality
│ ├── templates/core/ # HTML templates (menu, cart, checkout, etc.)
│ └── static/core/css/ # CSS styles for different pages
│
├── media/menu_images/ # Uploaded food images
├── manage.py
└── db.sqlite3 # Database file

---

## ⚙️ How to Run Locally

```bash
git clone https://github.com/SAMEERBHATTI4065/django-restaurant-website.git
cd django-restaurant-website
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


Then open your browser and go to:
http://127.0.0.1:8000/




