from django.contrib import admin
from adminapp import models
from userapp.models import ContactMessage
from userapp.models import CustomPaintingRequest
# Register your models here.

admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.Profile)
admin.site.register(CustomPaintingRequest)
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'subject', 'message')

    
