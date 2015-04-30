#-*- coding: utf-8 -*-
import json
import os
import copy
import logging
from random import shuffle
from time import time

from PyV8 import JSArray

from django.http import HttpResponse

from goldpoisk import js
from goldpoisk.serializer import JSONEncoder, BannerSerializer
from goldpoisk.cms.models import Banner
from goldpoisk.templates import get_menu, get_env
from goldpoisk.product.models import Product

logger = logging.getLogger('goldpoisk')

def main(req):
    logger.debug('Requesting main')

    products, count = Product.get_bids(1, 5)
    promo = Banner.objects.filter(hidden=False)
    if req.is_ajax():
        return HttpResponse(json.dumps({
            'promo': map(BannerSerializer().normalize, promo),
            'products': json.loads(products),
            'count': count
        }, cls=JSONEncoder))

    ctime = time()

    context = {
        'menu': get_menu(),
        'promo': map(BannerSerializer().normalize, promo),
        'products': json.loads(products),
        'count': count
    }
    context = json.dumps(context, cls=JSONEncoder)
    logger.info('Generating context: %gs' % (time() - ctime))

    ctime = time()
    html = js.render(context, 'pages["index.str"]', env=get_env())
    logger.info('Render: %gs' % (time() - ctime))

    res = HttpResponse(html);
    return res
