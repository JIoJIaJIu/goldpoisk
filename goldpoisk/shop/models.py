from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser

class Shop(models.Model):
    name = models.CharField(_('Name'), max_length=128)
    description = models.TextField(_('Description'), blank=True)
    url = models.URLField(_('Url'), blank=True, max_length=256)

    admin = models.ForeignKey('Admin', verbose_name=_('Admin'))

    class Meta:
        verbose_name = _('Shop')
        verbose_name_plural = _('Shops')

    def __unicode__(self):
        return self.name;

    @classmethod
    def get_types(cls, t):
        shops = cls.objects.filter(item__product__type=t).distinct('name')
        l = []
        for shop in shops:
            l.append({
                'id': shop.pk,
                'name': shop.name
            })
        return l

class Admin(AbstractBaseUser):
    email = models.EmailField(_("Email"), max_length=128, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password']

    class Meta:
        verbose_name = _('Admin')
        verbose_name_plural = _('Admins')

class Manager(AbstractBaseUser):
    email = models.EmailField(_("Email"), max_length=128, unique=True)
    shop = models.ForeignKey(Shop)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password']

    class Meta:
        verbose_name = _('Manager')
        verbose_name_plural = _('Managers')
