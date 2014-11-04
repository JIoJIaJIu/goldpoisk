from django.conf.urls import patterns, include, url

urlpatterns = patterns('goldpoisk.shop.views',
    url(r'^$', 'list'),
    url(r'^id(?P<id>\d+)$', 'shop'),
)
