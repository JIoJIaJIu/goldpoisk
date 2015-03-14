#-*- coding: utf-8 -*-
import os
import copy
import logging
from random import shuffle
from time import time
from PyV8 import JSClass, JSArray
from pybem import pybem

from django.http import HttpResponse
from django.conf import settings

from goldpoisk.templates import get_menu
from goldpoisk.product.models import get_products_for_main

class JS(JSClass):
    def log(self, *args):
        print args

renderer = pybem.BEMRender(os.path.abspath(settings.TEMPLATE_DIRS[0]), toplevelcls=JS)

logger = logging.getLogger(__name__)

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

    html = renderer.render('index', context, req, 'pages.index')
    logger.info('Render: %gs' % (time() - ctime))

    res = HttpResponse(html);
    return res

def best(req):
    context = {
        'menu': JSArray(get_menu()),
        'products': JSArray(get_products_for_main()),
    }

    html = renderer.render('index', context, req, 'pages.category')
    res = HttpResponse(html);
    return res
