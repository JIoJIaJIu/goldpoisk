from django.conf.urls import patterns, include, url

urlpatterns = patterns('product.views',
    url(r'^$', 'list'),
    url(r'^id(?P<id>\d+)$', 'product', name='product_item'),
)
