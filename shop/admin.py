from django.contrib import admin
from shop.models import Shop, Admin, Manager
from product.admin import HideFromIndex

admin.site.register(Shop)
admin.site.register(Admin)
admin.site.register(Manager)
