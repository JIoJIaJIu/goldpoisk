#-*- coding: utf-8 -*-
import logging
from time import time

from django.shortcuts import render
from django.http import HttpResponse

from goldpoisk.product.models import Type, Product
from goldpoisk.templates import get_renderer

logger = logging.getLogger('goldpoisk')

def category(req, category):
    logger.debug('Request')
    page = req.GET.get('page', 1)
    sort = req.GET.get('sort', None)

    countPerPage = 30
    products, count = Product.get_by_category(category, page, countPerPage, sort=sort)

    ctime = time()
    json = get_renderer().render('index', products, req, "blocks['g-goods.str']", return_bemjson=True)
    logger.info('Rendered %fs' % (time() - ctime))

    return HttpResponse(json, 'application/json')
