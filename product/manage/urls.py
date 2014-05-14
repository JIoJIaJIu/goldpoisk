from django.conf.urls import patterns, url

urlpatterns = patterns('product.manage.views',
    url('^$', 'admin'),
)
