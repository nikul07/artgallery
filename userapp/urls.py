from django.contrib import admin
from django.urls import path,include
from userapp import views
from .views import remove_from_cart

urlpatterns = [
     path('', views.userindexview, name="home"),

     path('userindexview/',views.userindexview,name="userindexview"),
     path('aboutview/',views.aboutview,name="aboutview"),
     path('cartview/',views.cartview,name="cartview"),
     path('checkoutview/',views.checkoutview,name="checkoutview"),
     path('usercontactview/', views.usercontactview, name='usercontact'),
     path('shopview/',views.shopview,name="shopview"),
     
     path('loginview/',views.loginview,name="loginview"),
     # path('adminregister/', views.adminregister, name="adminregister"),
     path('artistregisterview/',views.artistregisterview,name="artistregisterview"),
     path('registerview/', views.registerview, name="registerview"),
     path('logoutview/',views.logoutview,name="logoutview"),
     path("userprofileview/",views.userprofileview,name='userprofileview'),

     path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
     path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
     path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
     path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
     path('cart/cart_clear/<int:product_id>', views.cart_clear, name='cart_clear'),
     path('remove-from-cart/<str:item_id>/', remove_from_cart, name='remove_from_cart'),
     path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
     path('confirmOrderview/',views.confirmOrderview,name="confirmOrderview"),
     path('myorderview/',views.myorderview,name="myorderview"),
     path('increase_quantity/<str:item_id>/', views.increase_quantity, name='increase_quantity'),
     path('decrease_quantity/<str:item_id>/', views.decrease_quantity, name='decrease_quantity'),
     path('edit-profile/', views.edit_profile, name='edit_profile'),


     path('custom-painting-request/', views.custom_painting_request, name='custom_painting_request'),
     path('thank-you/', views.thank_you, name='thank_you'),
     

    
]
