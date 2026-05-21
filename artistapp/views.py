from django.shortcuts import render,redirect, get_object_or_404,HttpResponse
from adminapp import models
from django import forms
from django.contrib.auth.models import User
from adminapp.forms import ProductForm
from django.contrib import messages
from adminapp.models import Profile
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from adminapp.models import Product, Category

from django.shortcuts import render, redirect
# Create your views here.

def artistindexview(request):
    return render(request,'artistapp/artistindex.html')

# def artistindex2view(request):
    # return render(request,'artistapp/artistindex2.html')

def formbasicview(request):
    category = Category.objects.all()

    if request.method == 'POST':
        print("POST Data:", request.POST)
        print("FILES Data:", request.FILES)
        
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Artwork added successfully!")  # Success message
            return redirect('basictableview')  # Make sure this name is correct in urls.py
        else:
            print("Form.errors:", form.errors)
    else:
        form = ProductForm()

    context = {
        'category': category,
        'form': form,  # Pass the form to the template for rendering
    }

    return render(request, 'artistapp/form-basic.html', context)
    


def basictableview(request):
    products = Product.objects.all()  # Fetch all products from Product model
    context = {
        'products': products,  # Pass the products data to the template
    }
    return render(request, 'artistapp/basic-table.html', context)

def datatableview(request):
    return render(request,'artistapp/datatable.html')


def artistprofileview(request):
    
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)  # Safe access

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        image = request.FILES.get('image')

        # Update user
        if full_name:
            name_parts = full_name.split(' ')
            user.first_name = name_parts[0]
            user.last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
        if email:
            user.email = email
        user.save()

        # Update profile
        if phone:
            profile.phone = phone
        if image:
            profile.image = image
        profile.save()

        

        messages.success(request, "Profile updated successfully!")
        return redirect('artistprofile')

    return render(request,'artistapp/profile.html')

def artistloginview(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('artistindexview')
        elif user is not None and user.is_staff and user.is_superuser == False:
            login(request,user)
            return redirect('artistindexview')
        elif user is not None and user.is_superuser == False and user.is_staff == False:
            login(request,user)
            return redirect('artistindexview')
        else:
            return HttpResponse("user does not exist")

    return render(request,'userapp/login.html')

def artistlogoutview(request):
    logout(request)
    return redirect(artistloginview)

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
                User.objects.create_user(username=username,email=email,password=password,is_superuser=True,is_active=False)
                return redirect('artistloginview')
        else:
            return HttpResponse("password doesnt match")
    return render(request,'artistapp/artistregister.html')





def artist_update_view(request, id):
    category = models.Category.objects.all()
    product = get_object_or_404(Product, id=id)  # Get the product by ID
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('basictableview')  # Redirect after successful update
        else:
            print(form.errors)
    else:
        form = ProductForm(instance=product)

    return render(request, 'artistapp/artistupdate.html', {'form': form, 'product': product,'category':category})


def artist_delete_view(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.success(request, "Artwork deleted successfully!")
    return redirect('basictableview')

def artmanagecategories(request):
    category = models.Category.objects.all()
    category_count = category.count() 
    user_count = User.objects.count() 
    context = {'category':category,'category_count': category_count,'user_count': user_count }
    return render(request,'artistapp/manage_categories.html',context,)

def artupdatecategory(request, category_id):
    category = get_object_or_404(models.Category, id=category_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category.name = name
            category.save()
            return redirect('artmanagecategories')
    
    context = {'category': category}
    return render(request, 'artistapp/updatecategories.html', context)

def artdeletecategory(request, category_id):
    category = get_object_or_404(models.Category, id=category_id)
    category.delete()
    return redirect('artmanagecategories')

def artaddcategory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            models.Category.objects.create(name=name)
            return redirect('artmanagecategories')
    return render(request,'artistapp/artadd_categories.html')


