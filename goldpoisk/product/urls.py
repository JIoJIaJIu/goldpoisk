from django.conf.urls import patterns, include, url

from goldpoisk.ajax import views as ajax_views
from goldpoisk.templates import get_menu_regexp

urlpatterns = patterns('goldpoisk.product.views',
    url(get_menu_regexp(), 'category'),
    url(get_menu_regexp('/json'), ajax_views.category),
    url(r'^id(?P<id>\d+)$', 'product'),
    url(r'^id(?P<id>\d+)/json$', ajax_views.product),
)
