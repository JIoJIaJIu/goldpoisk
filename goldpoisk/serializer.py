import json
from decimal import Decimal


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

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return "%g" % o
        return super(JSONEncoder, self).default(o)
