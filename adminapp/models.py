from django.db import models
from django import forms
from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    Artimage = models.ImageField(upload_to='products/')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Quantity = models.PositiveIntegerField(default=0)
    Total = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def image(self):
        return self.Artimage


class Cart(models.Model):  # Ensure correct capitalization
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    phone = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=50, default='Admin')





