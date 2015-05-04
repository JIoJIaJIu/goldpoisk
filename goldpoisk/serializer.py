# -*- coding: utf8 -*-
import json
from decimal import Decimal

from django.db.models import Max

from goldpoisk.product.models import Image, Product, GemListSerializer

class BannerSerializer(object):
    def normalize(self, item):
        return {
            'src': item.get_absolute_url(),
            'title': item.name,  
            'items': map(PromotionSerializer().normalize, item.promotion_set.all()),
        }

    def serialize(self, item):
        pass

class PromotionSerializer(object):
    def normalize(self, promo):
        return {
            'x': promo.x,
            'y': promo.y,
            'price': promo.item.cost,
            'title': promo.item.product.name,
            # TODO:
            'url': promo.item.product.get_absolute_url(),
        }

class CustomsProductSerializer(object):
    def normalize(self, product):
        url = product.get_absolute_url()
        image = product.image_set.first()
        item = product.item_set.first() if product.count == 1 else None
        # TODO:
        carat = product.gems.all().aggregate(Max('carat'))['carat__max']
        return {
            'id': product.id,
            'title': product.name,
            'url': url,
            'image': image and image.get_absolute_url() or "blank.png",
            'number': product.number,
            'weight': '%g гр.' % product.weight,
            'count': product.count,
            # TODO:
            'carat': '%g' % carat if carat else None,
            'description': product.description,
            'minPrice': product.min_cost,
            'maxPrice': product.max_cost,
            'shopName': item and item.shop.name,
            'shopUrl': item and item.shop.url,
            'buyUrl': item and item.buy_url,

            'action': bool(product.action),
            'hit': bool(product.hit),
            'jsonUrl': url + '/json'
        }

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return "%g" % o
        return super(JSONEncoder, self).default(o)
