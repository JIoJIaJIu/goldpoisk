from django.conf.urls import patterns, url

urlpatterns = patterns('shop.manage.views',
    url('^$', 'admin'),
    url('^login$', 'login')
)
