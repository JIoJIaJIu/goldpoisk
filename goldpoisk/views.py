#-*- coding: utf-8 -*-
import os
import copy
import logging
from random import shuffle
from time import time
from PyV8 import JSClass, JSArray
from pybem import pybem

from django.http import HttpResponse

from goldpoisk.templates import get_menu, get_renderer
from goldpoisk.product.models import get_products_for_main


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

    ctime = time()
    context = {
        'menu': JSArray(get_menu()),
        'promo': JSArray(promo),
        'products': JSArray(get_products_for_main()),
    }
    logger.info('Generating context: %gs' % (time() - ctime))
    ctime = time()

    html = get_renderer().render('index', context, req, 'pages.index')
    logger.info('Render: %gs' % (time() - ctime))

    res = HttpResponse(html);
    return res

def best(req):
    context = {
        'menu': JSArray(get_menu()),
        'products': JSArray(get_products_for_main()),
    }

    html = get_renderer().render('index', context, req, 'pages.category')
    res = HttpResponse(html);
    return res
