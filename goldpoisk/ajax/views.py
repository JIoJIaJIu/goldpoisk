#-*- coding: utf-8 -*-
import json
import logging
from time import time

from django.shortcuts import render
from django.http import HttpResponse

from goldpoisk.product.models import Product, ProductSerializer
from goldpoisk import js

logger = logging.getLogger('goldpoisk')

def product(req, slug):
    logger.debug('Request %s' % req.path)
    try:
        product = Product.objects.prefetch_related('item_set').get(slug__exact=slug)
    except Product.DoesNotExist:
        return HttpResponse('{}', 'application/json')

    if not len(product.item_set.all()):
        return HttpResponse('{}', 'application/json')

    logger.debug('Serialize')
    product = ProductSerializer().serialize(product)

    return HttpResponse(product, 'application/json')

def GET_int(req, key):
    param = req.GET.get(key, None)
    if not param:
        return None

    def to_int(val):
        try:
            return int(val)
        except:
            pass

    return map(to_int, param.split('.'))
