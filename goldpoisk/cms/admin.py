from django.contrib import admin

from goldpoisk.cms.models import Banner, Promotion

class PromotionInline(admin.StackedInline):
    model = Promotion

class BannerAdmin(admin.ModelAdmin):
    inlines = [
        PromotionInline,
    ]

admin.site.register(Banner, BannerAdmin)
admin.site.register(Promotion)
