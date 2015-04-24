from django.conf.urls import patterns, include, url

from goldpoisk.ajax import views as ajax_views
from goldpoisk.templates import get_menu_regexp

urlpatterns = patterns('goldpoisk.product.views',
    url(get_menu_regexp(), 'category'),
    url(get_menu_regexp('/json'), ajax_views.category),
    url('^search$', 'search'),
    url(r'^products/json', 'products'),
    url(r'^item/(?P<slug>[\w\d-]+)$', 'product'),
    url(r'^item/(?P<slug>[\w\d-]+)/json$', ajax_views.product),
)
