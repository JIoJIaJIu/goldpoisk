from django.conf.urls import patterns, include, url

urlpatterns = patterns('shop.views',
    url(r'^$', 'list'),
    url(r'^id(?P<id>\d+)$', 'shop'),
)
