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
from goldpoisk.templates import get_menu, get_env
from goldpoisk.product.models import Product

logger = logging.getLogger('goldpoisk')

def main(req):
    logger.debug('Requesting main')
    promo = [
        'media/promotion/promotion_01.jpg',
        'media/promotion/promotion_02.jpg',
        'media/promotion/promotion_03.jpg',
        'media/promotion/promotion_04.jpg',
        'media/promotion/promotion_05.jpg',
        'media/promotion/promotion_06.jpg',
    ]
    shuffle(promo)
    products, count = Product.get_bids(1, 5)
    if req.is_ajax():
        return HttpResponse(json.dumps({
            'promo': promo,
            'products': json.loads(products),
            'count': count
        }))

    ctime = time()
    context = {
        'menu': JSArray(get_menu()),
        'promo': JSArray(promo),
        'products': js.eval(products),
        'count': count
    }
    logger.info('Generating context: %gs' % (time() - ctime))

    ctime = time()
    html = js.render(context, 'pages.index', env=get_env())
    logger.info('Render: %gs' % (time() - ctime))

    res = HttpResponse(html);
    return res
