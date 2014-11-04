from django.conf.urls import patterns, include, url

urlpatterns = patterns('goldpoisk.product.views',
    url(r'^$', 'list'),
    url(r'^id(?P<id>\d+)$', 'product'),
)
