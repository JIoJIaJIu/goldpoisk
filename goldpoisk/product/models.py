# -*- coding: utf-8 -*-
from os import path

from django.db import models
from django.db.models import Min, Max
from django.utils.translation import ugettext_lazy as _

from goldpoisk.settings import MEDIA_URL, UPLOAD_TO
from goldpoisk.shop.models import Shop

class Product(models.Model):
    type = models.ForeignKey('Type', verbose_name=_('Type'))
    name = models.CharField(_('Name'), max_length=128)
    description = models.TextField(_('Description'), blank=True)

    number = models.CharField(max_length=32)
    materials = models.ManyToManyField('Material', verbose_name=_('Materials'))
    gems = models.ManyToManyField('Gem', verbose_name=_('Gems'), blank=True)
    weight = models.PositiveIntegerField()

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __unicode__(self):
        return '%s "%s"' % (self.type.name, self.name)

    def get_weight(self):
        return '%d грамм' % self.weight

    def get_carat(self):
        carat = self.gems.all().aggregate(Max('carat'))['carat__max']
        if carat:
            carat = '%d карат' % carat
        return carat

    def get_absolute_url(self):
        return '/id%d' % self.pk

class Item(models.Model):
    cost = models.PositiveIntegerField(_('Cost'))
    quantity = models.PositiveSmallIntegerField(_('Quantity'))
    product = models.ForeignKey('Product', verbose_name=_('Type'))
    shop = models.ForeignKey(Shop, verbose_name=_('Shop'));
    buy_url = models.URLField(max_length=64, verbose_name=_('Buy url'))

    class Meta:
        verbose_name = _('Store product')
        verbose_name_plural = _('Store products')

    def __unicode__(self):
        return '%s: %d' % (self.product.__unicode__(), self.cost)


TYPE_CHOICES = (
    ('necklaces', 'necklaces'),
    ('chains', 'chains'),
    ('pendants','pendants'),
    ('bracelets','bracelets'),
    ('rings', 'rings'),
    ('earrings', 'earrings'),
    ('brooches', 'brooches'),
    ('watches', 'watches'),
    ('cutlery', 'cutlery'),
)

class Type(models.Model):
    name = models.CharField(max_length=128)
    url = models.SlugField(max_length=32)
    type = models.CharField(max_length=32, unique=True, choices=TYPE_CHOICES)

    def __unicode__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class Gem(models.Model):
    name = models.CharField(max_length=128)
    carat = models.PositiveIntegerField(blank=True)

    def __unicode__(self):
        return self.name

class Image(models.Model):
    src = models.ImageField(upload_to=UPLOAD_TO['product'])
    product = models.ForeignKey(Product)

    def get_absolute_url(self):
        return self.src.url

def get_products_for_category(category):
    products = Product.objects.filter(type__url__exact=category)
    products = products.annotate(min_cost=Min('item__cost'), max_cost=Max('item__cost'))

    return map(mapProduct, products)

def get_products_for_main():
    items = Item.objects.filter(quantity__gte=0)[:5]
    return map(mapItem, items)

def mapProduct(product):
    image = product.image_set.first()
    price = 0
    if hasattr(product, 'min_cost'):
        price = product.min_cost
    return {
        'title': product.name,
        'price': price,
        'image': image and image.get_absolute_url(),
        'href': product.get_absolute_url(),
        'pw': product.get_weight(),
        'jw': product.get_carat(),
    }

def mapItem(item):
    product = mapProduct(item.product)

    product.update({
        'shop': item.shop.name,
        'price': item.cost,
    })
    return product
