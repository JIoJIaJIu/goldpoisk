from django.conf.urls import patterns, include, url

from goldpoisk.templates import get_menu_regexp

urlpatterns = patterns('goldpoisk.product.views',
    url(get_menu_regexp(), 'category'),
    url(get_menu_regexp('/list'), 'category_ajax'),
    url(r'^id(?P<id>\d+)$', 'product'),
)
