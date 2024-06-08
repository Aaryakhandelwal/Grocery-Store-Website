from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.entry, name ='entry'),
    path('login_register', views.login_register, name ='login_register'),
    path('admin_login', views.admin_login, name ='admin_login'),
    path('user_login', views.user_login, name ='user_login'),
    path('seller_login', views.seller_login, name ='seller_login'),
    path('admin_register', views.admin_register, name='admin_register'),
    path('user_register', views.user_register, name='user_register'),
    path('seller_register', views.seller_register, name='seller_register'),
    path('admin_main_page', views.admin_main_page, name ='admin_main_page'),
    path('view_orders', views.view_orders, name ='view_orders'),
    path('add_delivery_boy', views.add_delivery_boy, name ='add_delivery_boy'),
    path('add_offers', views.add_offers, name ='add_offers'),
    path('add_seller', views.add_seller, name='add_seller'),
    path('add_product', views.add_product, name ='add_product'),
    path('seller_main_page', views.seller_main_page, name ='seller_main_page'),
    path('seller_add_category', views.seller_add_category, name ='seller_add_category'),
    path('seller_remove_category', views.seller_remove_category, name ='seller_remove_category'),
    path('seller_add_product', views.seller_add_product, name ='seller_add_product'),
    path('seller_remove_product', views.seller_remove_product, name ='seller_remove_product'),
    path('user_scroll_page', views.user_scroll_page, name ='user_scroll_page'),
    path('user_cart', views.user_cart, name ='user_cart'),
    path('user_checkout', views.user_checkout, name ='user_checkout'),
]
