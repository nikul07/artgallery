from django.shortcuts import render,redirect, get_object_or_404,HttpResponse
from adminapp import forms
from django.contrib.auth.models import User
from django.contrib.auth import logout,login,authenticate
from adminapp import models
from django.contrib import messages
from .models import Profile
from adminapp.forms import ProductForm
from artistapp.models import Artist



# Create your views here.

def indexview(request):
    user_count = User.objects.count()
    category_count = models.Category.objects.count()
    context = {
        'user_count': user_count,
        'category_count': category_count
        
    }
    return render(request,'adminapp/index.html',context)

def elementsview(request):
    return render(request,'adminapp/forms-elements.html')

def layoutsview(request):
    category = models.Category.objects.all()
    if request.method == 'POST':
        print("POST Data:", request.POST)
        print("FILES Data:", request.FILES)
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect(tblgeneralview)  # Ensure this name exists in urls.py
        else:
            print("Form.errors:", form.errors)
    context = {
        'category':category,
    }
    return render(request, 'adminapp/forms-layouts.html',context)

def updatecategoriesview(request):
    return render(request,'adminapp/updatecategories.html')

def addcategoriesview(request):
    return render(request,'adminapp/addcategories.html')


def validationview(request):
    return render(request,'adminapp/forms-validation.html')

def editorsview(request):
    return render(request,'adminapp/forms-editors.html')

def contactview(request):
    return render(request,'adminapp/pages-contact.html')

def adminregisterview(request):
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
                User.objects.create_user(username=username,email=email,password=password,is_superuser=True)
                return redirect('adminloginview')
        else:
            return HttpResponse("password doesnt match")
    return render(request,'adminapp/adminregister.html')

def adminloginview(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('indexview')
        elif user is not None and user.is_staff and user.is_superuser == False:
            login(request,user)
            return redirect('indexview')
        elif user is not None and user.is_superuser == False and user.is_staff == False:
            login(request,user)
            return redirect('indexview')
        else:
            return HttpResponse("user does not exist")
    return render(request,'userapp/login.html')

def adminlogoutview(request):
    logout(request)
    return redirect('adminloginview')

def tabledataview(request):
    return render(request,'adminapp/tables-data.html')

def tblgeneralview(request):
    p1 = models.Product.objects.all()
    print("Product:", p1)
    
    for i in p1:
        print("i", i.name, i.Artimage)
    
    return render(request, 'adminapp/tables-general.html', {'p1': p1})

def Admindelete(request,id):
    data = models.Product.objects.get(id=id)
    data.delete()
    return redirect(tblgeneralview)

def AdminUpdate(request, id):
    category = models.Category.objects.all()
    data = models.Product.objects.get(id=id)
    print("data:", data)

    if request.method == "POST":
        form = forms.ProductForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            print("Save successful")
            return redirect(tblgeneralview)  
        else:
            print("Form errors:", form.errors)
    context = {'data': data,'category':category} 
    return render(request, 'adminapp/update.html', context)


def adminprofileview(request):
    if request.user.is_authenticated:
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
            return redirect('adminprofileview')

        return render(request, 'adminapp/admin-profile.html', {'profile':profile})
    else:
        return redirect(adminloginview)


def addcategory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            models.Category.objects.create(name=name)
            return redirect('managecategories')
    return render(request,'adminapp/addcategories.html')

def managecategories(request):
    category = models.Category.objects.all()
    category_count = category.count() 
    user_count = User.objects.count() 
    context = {'category':category,'category_count': category_count,'user_count': user_count }
    return render(request,'adminapp/manage_categories.html',context,)

def updatecategory(request, category_id):
    category = get_object_or_404(models.Category, id=category_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category.name = name
            category.save()
            return redirect('managecategories')
    
    context = {'category': category}
    return render(request, 'adminapp/updatecategories.html', context)

def deletecategory(request, category_id):
    category = get_object_or_404(models.Category, id=category_id)
    category.delete()
    return redirect('managecategories')
#-----------------------------------------------------User Manage-------------------------------------------------------------------------------#
def usermanageview(request):
    users = User.objects.all()
    return render(request,'adminapp/usermanage.html', {'users': users})

def activate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    return redirect('usermanageview')

def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return redirect('usermanageview')

#--------------------------------------------------------------artist manage----------------------------------------------------------------------#

def artistmanageview(request):
    artists = Artist.objects.all()
    return render(request, 'adminapp/artistmanage.html', {'artists': artists})

def activate_artist(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    artist.is_active = True
    artist.save()
    return redirect('artistmanageview')

def deactivate_artist(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    artist.is_active = False
    artist.save()
    return redirect('artistmanageview')
#------------------------------------------------------------------------------------------------------------------------------------#
def contactmsg(request):
    return render(request,'adminapp/contactmessages.html')





