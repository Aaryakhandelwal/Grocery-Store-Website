from django.shortcuts import render, redirect, get_object_or_404
from home import models
from django.contrib import messages
from django.db.utils import OperationalError
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.db.models import F, ExpressionWrapper, FloatField
from decimal import Decimal
from .models import Offers
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
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # Check if user credentials exist in the database
            user = models.Customer.objects.get(Email_Address=email, password=password)
            # If user is found, store user ID in session and redirect to user main page or dashboard
            request.session['user_id'] = user.customer_id
            return redirect('user_scroll_page')
        except models.Customer.DoesNotExist:
            # If user is not found, render the login page with an error message
            return render(request, 'user_login.html', {'error': 'Invalid credentials. Please try again.'})

    return render(request, 'user_login.html')


def user_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        

        if models.Customer.objects.filter(Email_Address=email).exists():
            return render(request, 'user_register.html', {'error': 'User already exists. Try a different one!'})

        try:
             # Hash the password
            customer = models.Customer.objects.create(
                Name_of_the_customer=name,
                Delivery_Address=address,
                Email_Address=email,
                password=password,  # Hashed password
                Phone_number=phone
            )
            customer.save()
            return redirect('user_login')
        
        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'user_register.html', {'error': 'Database error. Please try again.'})
    return render(request, 'user_register.html')


def seller_login(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        # Check if a vendor with the provided phone number exists
        try:
            vendor = models.Vendor.objects.get(PhoneNumber=phone_number)
            return redirect('seller_add_product')
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


from django.db import transaction

@transaction.atomic
def user_scroll_page(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')  # Redirect to login if user is not authenticated
    
    items = models.Item.objects.all()

    if request.method == "POST":
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        item = get_object_or_404(models.Item, ProductID=item_id)
        
        customer = get_object_or_404(models.Customer, pk=user_id)
        cart, created = models.Cart.objects.get_or_create(customer=customer)
        cart_item, created = models.CartItem.objects.get_or_create(cart=cart, item=item)
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        
        # Update the quantity of the item in the main database
        item.Quantity -= quantity
        if (item.Quantity <= 0):
            item.delete()            
        else:
            item.save() 
        return redirect('user_scroll_page')

    return render(request, 'user_scroll_page.html', {'items': items})


from django.shortcuts import render, redirect, get_object_or_404
from . import models

from decimal import Decimal

def user_cart(request, discounted_price=None):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')  # Redirect to login if user is not authenticated

    customer = get_object_or_404(models.Customer, pk=user_id)
    cart = get_object_or_404(models.Cart, customer=customer)
    cart_items = models.CartItem.objects.filter(cart=cart)

    # Calculate total price for each item and update the cart_items queryset
    for item in cart_items:
        item.total_price = item.item.Price * item.quantity

    # Calculate the total price for the entire cart
    total_price = sum(item.total_price for item in cart_items)

    # Check if discounted price is available and save it in session
    if discounted_price is not None:
        request.session['discounted_price'] = float(discounted_price)  # Convert Decimal to float
    else:
        # If discounted price is None, set it equal to total price
        request.session['discounted_price'] = float(total_price)  # Convert Decimal to float

    # Save the total price in session
    request.session['total_price'] = float(total_price)  # Convert Decimal to float

    return render(request, 'user_cart.html', {
        'cart_items': cart_items,
        'total_price': float(total_price),  # Convert Decimal to float
        'discounted_price': float(request.session['discounted_price'])  # Convert Decimal to float
    })


def apply_offer(request):
    if request.method == 'POST':
        offer_code = request.POST.get('offer')
        try:
            # Retrieve the discount offer based on the offer code
            discount_offer = Offers.objects.get(PromoCode=offer_code)
            
            # Calculate the total price of the user's cart
            user_id = request.session.get('user_id')
            if not user_id:
                return redirect('user_login')  # Redirect to login if user is not authenticated
            
            customer = get_object_or_404(models.Customer, pk=user_id)
            cart = get_object_or_404(models.Cart, customer=customer)
            cart_items = models.CartItem.objects.filter(cart=cart)
            total_price = sum(item.item.Price * item.quantity for item in cart_items)
            
            # Calculate the discount based on the offer's percentage
            discount = (discount_offer.Percentage / 100) * float(total_price)

            # Check if the discount exceeds the MinOrderValue
            if discount > discount_offer.MinOrderValue:
                # Apply the discount to get the discounted price
                discounted_price = total_price - Decimal(discount)
                # Round off the discounted price to two digits
                discounted_price = round(discounted_price, 2)

                # Redirect to the user_cart view function with the discounted price as a parameter
                return redirect('user_cart', discounted_price=discounted_price)
            else:
                # If discount is less than or equal to MinOrderValue, do not apply the discount
                messages.error(request, "Discount cannot be applied. Minimum order value not met.")
        except Offers.DoesNotExist:
            # Handle case where offer code is invalid
            messages.error(request, "Invalid offer code.")
    # Handle GET requests or invalid offers
    return redirect('user_cart')


@transaction.atomic
def user_checkout(request):
    # Retrieve the user's cart items
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')  # Redirect to login if user is not authenticated
    
    customer = get_object_or_404(models.Customer, pk=user_id)
    cart = get_object_or_404(models.Cart, customer=customer)
    cart_items = models.CartItem.objects.filter(cart=cart)
    
    # Check if discounted price is available in session
    discounted_price = request.session.get('discounted_price')
    total_price = request.session.get('total_price')

    if not discounted_price or not total_price:
        # If discounted price or total price is not available in session, calculate them from the cart
        total_price = sum(item.item.Price * item.quantity for item in cart_items)
    
    # Pass the cart items, total price, discounted price, and customer's address to the template
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'discounted_price': discounted_price,
        'customer_address': customer.Delivery_Address  # Use the correct field name for the delivery address
    }
    
    return render(request, 'user_checkout.html', context)
from django.http import HttpResponseBadRequest
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from .models import CartItem

@transaction.atomic
def remove_from_cart_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity_to_remove_str = request.POST.get('quantity')
        
        if not item_id or not quantity_to_remove_str:
            return HttpResponseBadRequest("Item ID or quantity parameter is missing.")
        
        try:
            quantity_to_remove = int(quantity_to_remove_str)
            if quantity_to_remove <= 0:
                return HttpResponseBadRequest("Invalid quantity to remove. Quantity must be a positive integer.")
        except ValueError:
            return HttpResponseBadRequest("Invalid quantity to remove. Quantity must be a positive integer.")
        
        try:
            cart_item = CartItem.objects.get(id=item_id)
            current_quantity = cart_item.quantity
            
            if quantity_to_remove > current_quantity:
                return HttpResponseBadRequest("Requested quantity exceeds quantity in the cart.")
            
            new_quantity = current_quantity - quantity_to_remove
            
            item = cart_item.item
            item.Quantity += quantity_to_remove
            item.save()
            
            if new_quantity == 0:
                # If new quantity is zero or negative, remove item from cart
                cart_item.delete()
            else:
                # Update item quantity in the cart
                cart_item.quantity = new_quantity
                cart_item.save()
            
            return redirect('user_cart')
        
        except CartItem.DoesNotExist:
            return HttpResponseBadRequest("Cart item not found.")
    
    return HttpResponseBadRequest("Invalid request method.")
