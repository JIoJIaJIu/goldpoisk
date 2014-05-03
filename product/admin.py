from django.contrib import admin
from product.models import Product, Item, Type, Gem, Material, Image

class HideFromIndex(admin.ModelAdmin):
    def get_model_perms(self, *args, **kwargs):
        return {}

class ProductInline(admin.StackedInline):
    model = Product

class ItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(Item, ItemAdmin)

admin.site.register(Product, HideFromIndex)
admin.site.register(Type, HideFromIndex)
admin.site.register(Gem, HideFromIndex)
admin.site.register(Material, HideFromIndex)
admin.site.register(Image, HideFromIndex)
