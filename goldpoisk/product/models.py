# -*- coding: utf-8 -*-
from os import path
from PyV8 import JSArray
from time import time
import json

from django.db import models
from django.db.models import Min, Max, Count
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder, Serializer as JSONSerializer
from django.core.serializers import serialize
from django.core.paginator import Paginator

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
        #features.append({'Металл': self.materials.all()[0].name})

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

    @classmethod
    def _get_absolute_url(cls, pk):
        return '/id%d' % pk

    @classmethod
    def get_by_category(cls, category, page=1, countPerPage=20, sort=None):
        c = time()
        products = cls.objects.prefetch_related('image_set').filter(type__url__exact=category, item__isnull=False)
        products = products.annotate(count=Count('item'), min_cost=Min('item__cost'), max_cost=Max('item__cost'), carat=Max('gems__carat'))
        #TODO: optimize
        count = products.aggregate(count=Count('number'))['count']
        if sort:
            key = {
                'price': lambda: products.order_by('max_cost'),
                'tprice': lambda: products.order_by('-min_cost'),
                'name': lambda: products.order_by('name'),
            }[sort]
            if key:
                products = key()

        products = products.values(
            'pk',
            'name',
            'count',
            'number',
            'description',
            'weight',
            'min_cost',
            'max_cost',
            'item__shop__name',
            'item__shop__url',
            'item__buy_url',
            'image__src',
            'item__action',
            'item__hit',
            'carat',
        )
        paginator = Paginator(products, countPerPage)
        print 'Request %fs' % (time() - c)

        c = time()
        json = ProductSerializer().serialize(paginator.page(page).object_list)
        print 'Serializer %fs' % (time() - c)

        return json, count

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

    @classmethod
    def _get_absolute_url(cls, src):
        return '/media/%s' % src 

def get_products_for_main():
    bids = BestBid.objects.all().prefetch_related('item')
    return map(mapItem, [bid.item for bid in bids])

def mapProduct(product):
    images = product.image_set
    image = images.first()
    price = 0
    if hasattr(product, 'min_cost'):
        price = product.min_cost
    return {
        'title': product.name,
        'number': product.number,
        'price': price,
        'image': image and image.get_absolute_url(),
        'images': JSArray(map(lambda x: x.get_absolute_url(), images.all()) ),
        'url': product.get_absolute_url(),
        'weight': product.get_weight(),
        'carat': product.get_carat(),
    }

def mapItem(item):
    data = {
        'store': item.shop.name,
        'storeUrl': item.shop.url,
        'price': item.cost,
        'buyUrl': item.buy_url,
        'count': 1
    }

    data.update(mapProduct(item.product))

    try:
        item.action is not None
        data.update({
            'action': True
        })
    except ObjectDoesNotExist:
        pass

    try:
        item.hit is not None
        data.update({
            'hit': True
        })
    except ObjectDoesNotExist:
        pass

    return data

class ProductSerializer(object):
    def serialize(self, products):
        l = []
        for p in products:
            #TODO:
            if p['carat']:
                carat = "%g" % p['carat']
            else:
                carat = None
            l.append({
                'title': p['name'],
                'count': p['count'],
                'image': Image._get_absolute_url(p['image__src']),
                'url': Product._get_absolute_url(p['pk']),
                'carat': carat,
                'number': p['number'],
                'weight': '%g гр.' % p['weight'],
                'minPrice': p['min_cost'],
                'maxPrice': p['max_cost'],
                'shopName': p['item__shop__name'],
                'shopUrl': p['item__shop__url'],
                'buyUrl': p['item__buy_url'],
                'action': bool(p['item__action']),
                'hit': bool(p['item__hit']),
            })
        return json.dumps(l)
