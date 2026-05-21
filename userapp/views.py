from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from adminapp.models import Product,Category
from userapp import forms 
from userapp import models
from artistapp.views import artistindexview
from userapp.forms import ContactForm
from django.contrib import messages
from userapp.models import CustomPaintingRequest


# Create your views here.

def userindexview(request):
    products = Product.objects.all()  # Corrected model reference
    context = {'products': products}
    return render(request,'userapp/userindex.html',context)

def aboutview(request):
    return render(request,'userapp/about.html')

def cartview(request):
    carts = Cart(request)  # Get cart instance
    print("cart", carts)
    cart_items = list(carts.cart.values())  # Ensure it's a list
    print("item", cart_items)
    total = 0
    subtotal = 0
    for ab in carts.cart.values():
        price = float(ab['price'])
        quantity = float(ab['quantity'])
        subtotal = price * quantity
        total += subtotal
    
    print(subtotal)
    print(total)
    shipping = (total * 5)/100
    total = total + shipping
    context = {
        'subtotal': subtotal,
        'total': total,
        'shipping': shipping,
    }

    return render(request, 'userapp/cart.html', context)


def checkoutview(request):
    carts = Cart(request)  # Get cart instance
    print("cart", carts)
    cart_items = list(carts.cart.values())  # Ensure it's a list
    print("item", cart_items)
    total = 0
    for ab in carts.cart.values():
        price = float(ab['price'])
        quantity = float(ab['quantity'])
        subtotal = price * quantity
        total += subtotal

    shipping = (total * 5)/100
    total = total + shipping

    if request.method == "POST":
        total = 0
        fnl = models.FinalOrder.objects.create(user=request.user,total=0)
        for ab in carts.cart.values():
            price = float(ab['price'])
            quantity = float(ab['quantity'])
            subtotal = price * quantity
            total += subtotal
            product_data = models.Product.objects.get(id=ab['product_id'])
            conf_order = models.ConfirmOrder.objects.create(final=fnl,
                                                            product=product_data,
                                                            subtotal=subtotal,
                                                            quantity = quantity,
                                                            )
            print(conf_order)

        form = forms.BillingAddressForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.final = fnl 
            obj.save()
        else:
            print(form.errors)
        
        fnl.total = total
        fnl.save()
        carts.clear()
        return redirect(confirmOrderview)

    context = {
        'subtotal': subtotal,
        'total': total,
        'shipping': shipping,
    }
    return render(request,'userapp/checkout.html',context)

def usercontactview(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('usercontact')  # Make sure 'usercontact' matches your URL name
        else:
            messages.error(request, 'There was an error in your form. Please correct it below.')
    else:
        form = ContactForm()
    return render(request, 'userapp/contact.html', {'form': form})

def shopview(request):
    category = Category.objects.all()  # Corrected model reference
    category_id = request.GET.get('category_id')
    print("category_id",category_id)
    products = Product.objects.all()  
    if category_id:
        products = Product.objects.filter(category__id=category_id)
    context = {'products': products,'category':category,'category_id':category_id}  # Updated context key to be plural
    return render(request, 'userapp/shop.html', context)

# @login_required
def loginview(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('indexview')
        elif user is not None and user.is_staff and user.is_superuser == False:
            login(request,user)
            return redirect(artistindexview)
        elif user is not None and user.is_superuser == False and user.is_staff == False:
            login(request,user)
            return redirect(userindexview)
        else:
            return HttpResponse("user does not exist")

    return render(request,'userapp/login.html')


def logoutview(request):
    logout(request)
    return redirect(loginview)

# def adminregister(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         password1 = request.POST.get('password1')
#         if password == password1:
#             try:
#                 User.objects.get(username=username)
#                 return HttpResponse("username already exists")
#             except User.DoesNotExist:
#                 User.objects.create_user(username=username,email=email,password=password,is_superuser=True)
#                 return redirect('loginview')
#         else:
#             return HttpResponse("password doesnt match")
#     return render(request,'userapp/adminregister.html')

def registerview(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        if password == password1:
            try:
                User.objects.get(username=username)
                return HttpResponse("username already exists")
            except User.DoesNotExist:
                User.objects.create_user(username=username,email=email,password=password)
                return redirect('loginview')
        else:
            return HttpResponse("password doesnt match")    
    return render (request, "userapp/register.html")

def artistregisterview(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        if password == password1:
            try:
                User.objects.get(username=username)
                return HttpResponse("username already exists")
            except User.DoesNotExist:
                User.objects.create_user(username=username,
                                         email=email,
                                         is_staff=True,
                                         password=password)
                return redirect('loginview')
        else:
            return HttpResponse("password doesnt match")  
    return render(request,'artistapp/register.html')

def userprofileview(request):
    return render(request, 'userapp/profile.html')

def cart_add(request, product_id):
    print("hii")
    product_detail = get_object_or_404(Product, id=product_id)
    print("product",product_detail)
    cart = Cart(request)
    print("cart",cart)
    product = Product.objects.get(id=product_id)
    print("pro",product)
    cart.add(product=product_detail)
    return redirect("cartview",)



def item_clear(request, id):
    print("hii")
    cart = Cart(request)
    print("cart",cart)
    Product = Product.objects.get(id=id)
    print("product",Product)
    cart.remove(Product)
    return redirect("cart_detail")



def item_increment(request, id):
    cart = Cart(request)
    Product = Product.objects.get(id=id)
    cart.add(product=Product)
    return redirect("cart_detail")



def item_decrement(request, id):
    cart = Cart(request)
    Product = Product.objects.get(id=id)
    cart.decrement(Product=Product)
    return redirect("cart_detail")



def cart_clear(request, product_id):
    cart = Cart(request)
    cart.clear(product_id)
    return redirect("cartview")


def cart_detail(request):
    return render(request, 'cart/cart_detail.html')

def confirmOrderview(request):
    return render(request, 'userapp/confirmOrder.html')

def myorderview(request):
    final_orders = models.FinalOrder.objects.filter(user=request.user).order_by('-id')
    all_confirm_orders = []

    for final in final_orders:
        confirm_order = models.ConfirmOrder.objects.filter(final=final)
        all_confirm_orders.append({
            'final': final,
            'items': confirm_order,
        })

    context = {
        'all_orders': all_confirm_orders,
    }
    return render(request, 'userapp/myorder.html', context)


def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})

    if item_id in cart:
        del cart[item_id]  # Remove the item from the cart

    request.session['cart'] = cart  # Save the updated cart back to session
    return redirect('cartview')  # Redirect back to the cart page

def increase_quantity(request, item_id):
    cart = request.session.get('cart', {})
    if item_id in cart:
        cart[item_id]['quantity'] += 1
        request.session['cart'] = cart
    return redirect('cartview')  # Replace with your cart view name

def decrease_quantity(request, item_id):
    cart = request.session.get('cart', {})
    if item_id in cart:
        if cart[item_id]['quantity'] > 1:
            cart[item_id]['quantity'] -= 1
        else:
            del cart[item_id]  # Remove item if quantity is 1
        request.session['cart'] = cart
    return redirect('cartview')  # Replace with your cart view name

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        return redirect('userprofileview')  # After saving, go back to profile
    return render(request, 'userapp/edit_profile.html')

# ____________________________________Customize painting_______________________________________________________________________
def custom_painting_request(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        description = request.POST['description']
        size = request.POST['size']
        reference_image = request.FILES.get('reference_image')

        request_obj = CustomPaintingRequest(
            name=name,
            email=email,
            description=description,
            size=size,
            reference_image=reference_image
        )
        request_obj.save()
        return render(request, 'userapp/thankyou.html', {'name': name})

    return render(request, 'userapp/customizePaintings.html')

def thank_you(request):
    return render(request, 'thankyou.html')
            
# ________________________________________End________________________________________________________







