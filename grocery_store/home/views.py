from django.shortcuts import render, redirect
from home import models
import mysql.connector

def entry(request):
    return render(request, 'entry.html')

def login_register(request):
    return render(request, 'login_register.html')

def admin_login(request):
    return render(request, 'admin_login.html')

def admin_register(request):
    if request.method == 'POST':
        admin_name = request.POST.get('admin_name')
        password = request.POST.get('password')
        admin = models.Admin(Admin_Name=admin_name, password=password)
        admin.save()
        return redirect('registration_success')  
    return render(request, 'admin_register.html')

def user_login(request):
    return render(request, 'user_login.html')

def user_register(request):
    return render(request, 'user_register.html')

def seller_login(request):
    return render(request, 'seller_login.html')

def seller_register(request):
    return render(request, 'seller_register.html')

def admin_main_page(request):
    return render(request, 'admin_main_page.html')

def view_orders(request):
    return render(request, 'view_orders.html')\
        
def add_delivery_boy(request):
    return render(request, 'add_delivery_boy.html')

def seller_add_category(request):
    return render(request, 'seller_add_category.html')

def seller_remove_category(request):
    return render(request, 'seller_remove_category.html')


def add_offers(request):
    return render(request, 'add_offers.html')


def add_product(request):
    return render(request, 'add_product.html')

def seller_add_product(request):
    return render(request, 'seller_add_product.html')

def register(request):
    return render(request, 'register.html')

def seller_main_page(request):
    return render(request, 'seller_main_page.html')


def seller_remove_product(request):
    return render(request, 'seller_remove_product.html')

def add_seller(request):
    return render(request, 'add_seller.html')

def user_scroll_page(request):
    return render(request, 'user_scroll_page.html')

def user_cart(request):
    return render(request, 'user_cart.html')

def user_checkout(request):
    return render(request, 'user_checkout.html')