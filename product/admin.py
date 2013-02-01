from django.contrib import admin
from product.models import Product, Item, Type, Gem, Material, Image

class ImageInline(admin.StackedInline):
    model = Image

class ProductAdmin(admin.ModelAdmin):
    inlines = [ ImageInline ]

admin.site.register(Product, ProductAdmin)
admin.site.register(Item)
admin.site.register(Type)
admin.site.register(Gem)
admin.site.register(Material)
