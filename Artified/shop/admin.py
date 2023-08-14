from django.contrib import admin
from . models import *
from django.contrib.auth.admin import UserAdmin



admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderUpdate)
admin.site.register(Seller)
admin.site.register(Product_image)
admin.site.register(CustomUser, UserAdmin)