from django.db import models
from django.utils.translation import ugettext_lazy as _

from goldpoisk.settings import UPLOAD_TO
from shop.models import Shop

class Product(models.Model):
    type = models.ForeignKey('Type', verbose_name=_('Type'))
    name = models.CharField(_('Name'), max_length=128)
    description = models.TextField(_('Description'), blank=True)

    materials = models.ManyToManyField('Material', verbose_name=_('Materials'))
    gems = models.ManyToManyField('Gem', verbose_name=_('Gems'))

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __unicode__(self):
        return '%s "%s"' % (self.type.name, self.name)

class Item(models.Model):
    cost = models.PositiveIntegerField(_('Cost'))
    quantity = models.PositiveSmallIntegerField(_('Quantity'))
    product = models.ForeignKey('Product', verbose_name=_('Type'))
    shop = models.ForeignKey(Shop, verbose_name=_('Shop'));

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __unicode__(self):
        return '%s: %d' % (self.product.__unicode__(), self.cost)


class Type(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class Gem(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class Image(models.Model):
    src = models.ImageField(upload_to=UPLOAD_TO['product'])
    product = models.ForeignKey(Product)
