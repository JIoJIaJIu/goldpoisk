from django.contrib import admin
from product.models import Product, Item, Type, Gem, Material, Image

class HideFromIndex(admin.ModelAdmin):
    def get_model_perms(self, *args, **kwargs):
        return {}

class ImageInline(admin.StackedInline):
    model = Image

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline
    ]

admin.site.register(Item)

admin.site.register(Product, ProductAdmin)
admin.site.register(Type, HideFromIndex)
admin.site.register(Gem, HideFromIndex)
admin.site.register(Material, HideFromIndex)
admin.site.register(Image, HideFromIndex)
