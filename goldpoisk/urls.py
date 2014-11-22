from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static

from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'alljewel.views.home', name='home'),
    # url(r'^alljewel/', include('alljewel.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^penal/', include(admin.site.urls)),
    url(r'^shops/', include('goldpoisk.shop.urls')),
    url(r'^manage/', include('goldpoisk.shop.manage.urls')),
    url(r'^$', 'goldpoisk.views.main'),
    url(r'^', include('goldpoisk.product.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static('css', document_root=settings.STATIC_ROOT + 'css')
    urlpatterns += static('images', document_root=settings.STATIC_ROOT + 'images')
