# -*- coding: utf-8 -*-
from os import path

from django.db import models
from django.db.models import Min, Max, Count
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from goldpoisk.settings import MEDIA_URL, UPLOAD_TO
from goldpoisk.shop.models import Shop
from goldpoisk.models import BestBid

class Product(models.Model):
    type = models.ForeignKey('Type', verbose_name=_('Type'))
    name = models.CharField(_('Name'), max_length=128)
    description = models.TextField(_('Description'), blank=True)

    number = models.CharField(max_length=32)
    materials = models.ManyToManyField('Material', verbose_name=_('Materials'))
    gems = models.ManyToManyField('Gem', verbose_name=_('Gems'), blank=True)
    weight = models.DecimalField(decimal_places=5, max_digits=8)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __unicode__(self):
        return '%s %s' % (self.name, self.number)

    def get_weight(self):
        return '%g грамм' % self.weight

    def get_carat(self):
        carat = self.gems.all().aggregate(Max('carat'))['carat__max']
        if carat:
            return '%g карат' % carat
        return None

    def get_features(self):
        features = []
        features.append({'Артикул': self.number})
        features.append({'Металл': self.materials.all()[0].name})

        gems = []
        carats = []
        for gem in self.gems.all()[:3]:
            gems.append(gem.name)
            if gem.carat:
                carats.append('%g' % gem.carat)
            else:
                carats.append('*')

        if len(gems):
            features.append({'Камень': ', '.join(gems)})
            features.append({'Карат': ', '.join(carats)})

        return features

    def get_absolute_url(self):
        return '/id%d' % self.pk

class Item(models.Model):
    cost = models.PositiveIntegerField(_('Cost'))
    quantity = models.PositiveSmallIntegerField(_('Quantity'))
    product = models.ForeignKey('Product', verbose_name=_('Type'))
    shop = models.ForeignKey(Shop, verbose_name=_('Shop'));
    buy_url = models.URLField(max_length=256, verbose_name=_('Buy url'))

    class Meta:
        verbose_name = _('Store product')
        verbose_name_plural = _('Store products')

    def __unicode__(self):
        return u'%s: %d руб' % (self.product.__unicode__(), self.cost)


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
    carat = models.DecimalField(decimal_places=5, max_digits=8, blank=True)

    def __unicode__(self):
        if self.carat:
            return '%s %.3f' % (self.name, self.carat)
        return self.name

class Image(models.Model):
    src = models.ImageField(upload_to=UPLOAD_TO['product'])
    product = models.ForeignKey(Product)

    def get_absolute_url(self):
        return self.src.url

def get_products_for_category(category):
    products = Product.objects.filter(type__url__exact=category, item__isnull=False)
    def eachProduct(product):
        items = product.item_set.all()
        if len(items) == 1:
            return mapItem(items[0])

        return mapProduct(product)
    #products = products.annotate(min_cost=Min('item__cost'), max_cost=Max('item__cost'))

    return map(eachProduct, products)

def get_products_for_main():
    bids = BestBid.objects.all().prefetch_related('item')
    return map(mapItem, [bid.item for bid in bids])

def mapProduct(product):
    image = product.image_set.first()
    price = 0
    if hasattr(product, 'min_cost'):
        price = product.min_cost
    return {
        'title': product.name,
        'price': price,
        'imageUrl': image and image.get_absolute_url(),
        'url': product.get_absolute_url(),
        'weight': product.get_weight(),
        'carat': product.get_carat(),
    }

def mapItem(item):
    product = mapProduct(item.product)

    product.update({
        'store': item.shop.name,
        'storeUrl': item.shop.url,
        'price': item.cost,
        'buyUrl': item.buy_url
    })

    try:
        item.action is not None
        product.update({
            'action': True
        })
    except ObjectDoesNotExist:
        pass

    try:
        item.hit is not None
        product.update({
            'hit': True
        })
    except ObjectDoesNotExist:
        pass

    return product
