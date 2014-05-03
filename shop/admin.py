from django.contrib import admin
from shop.models import Shop, Admin
from product.admin import HideFromIndex

admin.site.register(Shop)
admin.site.register(Admin, HideFromIndex) 
