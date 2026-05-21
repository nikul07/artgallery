from django.contrib import admin
from userapp import models
# Register your models here.

admin.site.register(models.BillingAddress)
admin.site.register(models.FinalOrder)
admin.site.register(models.ConfirmOrder)