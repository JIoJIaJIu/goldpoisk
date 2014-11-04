from django.contrib import admin
from goldpoisk.shop.models import Shop, Admin, Manager
from goldpoisk.product.admin import HideFromIndex

admin.site.register(Shop)
admin.site.register(Admin)
admin.site.register(Manager)
