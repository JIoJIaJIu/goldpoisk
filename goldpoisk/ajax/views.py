#-*- coding: utf-8 -*-
import json
import logging
from time import time

from django.shortcuts import render
from django.http import HttpResponse

from goldpoisk.product.models import Type, Product, ProductSerializer
from goldpoisk import js

logger = logging.getLogger('goldpoisk')

def category(req, category):
    logger.debug('Request %s' % req.path)
    page = req.GET.get('page', 1)
    sort = req.GET.get('sort', None)
    filters = {
        'gems': GET_int(req, 'gem'),
        'shops': GET_int(req, 'store'),
        'materials': GET_int(req, 'material'),
    }

    countPerPage = 30
    products, count = Product.get_by_category(category, page, countPerPage, sort=sort, filters=filters)
    products = json.dumps({
        'list': json.loads(products),
        'count': count,
    })
    return HttpResponse(products, 'application/json')

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
