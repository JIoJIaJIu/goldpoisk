from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Shop(models.Model):
    name = models.CharField(_('Name'), max_length=128)
    description = models.TextField(_('Description'), blank=True)

    admin = models.ForeignKey('Admin', verbose_name=_('Admin'))

    class Meta:
        verbose_name = _('Shop')
        verbose_name_plural = _('Shops')

class Admin(User):
    pass

class Manager(models.Model):
    shop = models.ForeignKey(Shop)
