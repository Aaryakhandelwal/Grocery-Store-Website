from django.shortcuts import render, redirect
from home import models
from django.contrib import messages
from django.db.utils import OperationalError
from django.db import IntegrityError



def entry(request):
    return render(request, 'entry.html')

def login_register(request):
    return render(request, 'login_register.html')



def admin_login(request):
    if request.method == 'POST':
        admin_name = request.POST.get('admin_name')
        password = request.POST.get('password')
        try:
            # Check if admin credentials exist in the database
            admin = models.Admin.objects.get(Admin_Name=admin_name, password=password)
            # If admin is found, redirect to admin dashboard or home page
            return redirect('view_orders') 
        except models.Admin.DoesNotExist:
            # If admin is not found, render the login page with an error message
            return render(request, 'admin_login.html', {'error': 'Invalid credentials. Please try again.'})

    return render(request, 'admin_login.html')


def admin_register(request):
    if request.method == 'POST':
        admin_name = request.POST.get('admin_name')
        password = request.POST.get('password')
        if models.Admin.objects.filter(Admin_Name = admin_name).exists():
            return render(request, 'admin_register.html', {'error': 'Username already exists. Try a different one!'})
        try:
            # Create a new Admin object and save it to the database
            admin = models.Admin.objects.create(Admin_Name=admin_name, password=password)
            admin.save()
            return redirect('admin_login')
        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'admin_register.html', {'error': 'Database error. Please try again.'})
        
    return render(request, 'admin_register.html')


def user_login(request):
    return render(request, 'user_login.html')

def user_register(request):
    return render(request, 'user_register.html')


def seller_login(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        # Check if a vendor with the provided phone number exists
        try:
            vendor = models.Vendor.objects.get(PhoneNumber=phone_number)
            return redirect('seller_main_page')
        except models.Vendor.DoesNotExist:
            # If vendor does not exist, show login failure message or redirect to login page again
            return render(request, 'seller_login.html', {'error':"Seller with this phone number does not exist. Please ask the admin."})
        
    return render(request, 'seller_login.html')
    



def admin_main_page(request):
    return render(request, 'admin_main_page.html')



def view_orders(request):
    orders = models.Order.objects.all()
    return render(request, 'view_orders.html', {'orders': orders})
        
def add_delivery_boy(request):
    if request.method == 'POST':
        boy_name = request.POST.get('name')
        boy_phone = request.POST.get('phone')
        boy_vehicle = request.POST.get('vehicle')
        if models.DeliveryBoy.objects.filter(PhoneNumber = boy_phone).exists():
            return render(request, 'add_delivery_boy.html', {'error': 'Delivery Partner already exists. Try a different one!'})
        try:
            boy = models.DeliveryBoy.objects.create(Name=boy_name, PhoneNumber=boy_phone, Vehicle=boy_vehicle )
            boy.save()
            return render(request, 'add_delivery_boy.html', {'success': 'Delivery Partner successfully added!'})
        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'add_delivery_boy.html', {'error': 'Database error. Please try again.'})
        
    return render(request, 'add_delivery_boy.html')

def add_offers(request):
    if request.method == 'POST':
        promo_code = request.POST.get('promo_code')
        discount_percentage = request.POST.get('discount_percentage')
        min_order_value = request.POST.get('min_order_value')

        if models.Offers.objects.filter(PromoCode = promo_code).exists():
            return render(request, 'add_offers.html', {'error': 'Offer already exists. Try a different one!'})
        try:
            offer = models.Offers.objects.create(PromoCode = promo_code, Percentage = discount_percentage, MinOrderValue = min_order_value)
            offer.save()
            return render(request, 'add_offers.html', {'success': 'Offer added successfully!'})
        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'add_offers.html', {'error': 'Database error. Please try again.'})
        
    return render(request, 'add_offers.html')

def view_products(request):
    item = models.Item.objects.all()
    return render(request, 'view_products.html', {'items': item})

def add_seller(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        if models.Vendor.objects.filter(PhoneNumber = phone).exists():
            return render(request, 'add_seller.html', {'error': 'Seller already exists. Try a different one!'})
        try:
            seller = models.Vendor.objects.create(Name=name, PhoneNumber = phone, Address = address)
            seller.save()
            return render(request, 'add_seller.html', {'success': 'Seller added successfully!'})
        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'add_seller.html', {'error': 'Database error. Please try again.'})

    return render(request, 'add_seller.html')


def seller_add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('categoryName')
        try:
            new_category = models.Category(Category_Name=category_name)
            new_category.save()
            return render(request, 'seller_add_category.html', {'success': 'Category added successfully!'})
        except IntegrityError:
            return render(request, 'seller_add_category.html', {'error': 'Category with this name already exists.'})
        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'seller_add_category.html', {'error': 'Database error. Please try again.'})

    return render(request, 'seller_add_category.html')

def seller_remove_category(request):
    categories = models.Category.objects.all()  # Retrieve all categories
    if request.method == 'POST':
        category_id = request.POST.get('categoryId')
        try:
            category = models.Category.objects.get(CategoryID=category_id)
            category.delete()
            return render(request, 'seller_remove_category.html', {'categories': categories, 'success': 'Category removed successfully!'})
        except models.Category.DoesNotExist as e:
            print(f"Error: {e}")
            return render(request, 'seller_remove_category.html', {'categories': categories, 'error': 'Category does not exist!'})
    return render(request, 'seller_remove_category.html', {'categories': categories})


def seller_add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_name = request.POST.get('category')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        try:
            # Check if category exists
            if not models.Category.objects.filter(Category_Name=category_name).exists():
                return render(request, 'seller_add_product.html', {'error': 'Category doesn\'t exist. Add category or try again!'})

            # Get the category instance
            category = models.Category.objects.get(Category_Name=category_name)

            # Create and save the item
            item = models.Item.objects.create(
                Name_of_the_item=name,
                Description=description,
                CategoryID=category,
                Price=price,
                Quantity=quantity
            )
            item.save()

            return render(request, 'seller_add_product.html', {'success': 'Product added successfully!'})

        except OperationalError as oe:
            print(f"Operational Error: {oe}")
            return render(request, 'seller_add_product.html', {'error': 'Category table does not exist. Please create the category table and try again!'})
        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'seller_add_product.html', {'error': 'Database error. Please try again.'})

    return render(request, 'seller_add_product.html')


def register(request):
    return render(request, 'register.html')

def seller_main_page(request):
    return render(request, 'seller_main_page.html')


def seller_remove_product(request):
    products = models.Item.objects.all()  # Retrieve all products
    if request.method == 'POST':
        product_id = request.POST.get('productId')
        try:
            product = models.Item.objects.get(ProductID=product_id)
            product.delete()
            # Redirect to a success page or display a success message
            return render(request, 'seller_remove_product.html', {'success': 'Product removed successfully!'})
        except models.Item.DoesNotExist as e:
            print(f"Error: {e}")
            return render(request, 'seller_add_product.html', {'error': 'Product does not exist!'})
    return render(request, 'seller_remove_product.html', {'products': products})


def user_scroll_page(request):
    return render(request, 'user_scroll_page.html')

def user_cart(request):
    return render(request, 'user_cart.html')

def user_checkout(request):
    return render(request, 'user_checkout.html')