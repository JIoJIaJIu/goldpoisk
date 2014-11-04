from django.conf.urls import patterns, url

urlpatterns = patterns('goldpoisk.shop.manage.views',
    url('^$', 'admin'),
    url('^login$', 'login')
)
