from django.db import models
from django.contrib.auth.models import User
from adminapp.models import Product

# Create your models here.


class FinalOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    total = models.FloatField()

class ConfirmOrder(models.Model):
    final = models.ForeignKey(FinalOrder,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    subtotal = models.FloatField()
    quantity = models.IntegerField() 


class BillingAddress(models.Model):
    final = models.ForeignKey(FinalOrder,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.BigIntegerField()
    address = models.TextField()
    description = models.TextField(null=True,blank=True)


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()

class CustomPaintingRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()
    reference_image = models.ImageField(upload_to='custom_requests/', blank=True, null=True)
    size = models.CharField(max_length=20, choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')])
    status = models.CharField(max_length=20, default='Pending')  # Pending, In Progress, Completed
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.name} ({self.status})"

