import copy
import os
from PyV8 import JSArray
from pybem import pybem

from django.http import HttpResponse, Http404
from django.db.models import Min, Max

from goldpoisk import settings
from goldpoisk.product.models import Item, Product, get_products_for_category
from goldpoisk.templates import get_menu, get_with_active_menu

renderer = pybem.BEMRender(os.path.abspath(settings.TEMPLATE_DIRS[0]))

def category(req, category):
    context = {
        'menu': JSArray(get_with_active_menu(category)),
        'products': JSArray(get_products_for_category(category))
    }

    html = renderer.render('index', context, req, 'pages.category')

    res = HttpResponse(html)
    return res

def product(req, id):
    try:
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        raise Http404

    category = product.type
    images = product.image_set.all()
    context = {
        'menu': JSArray(get_with_active_menu(category.url)),
        'item': {
            'title': product.name,
            'category': product.type.name,
            'gallery': {
                'images': JSArray(map(lambda i: i.get_absolute_url(), images)),
                'mainImg': images[0].get_absolute_url(),
            },
            'features': JSArray(product.get_features()),
            'description': product.description,
        },
    }

    html = renderer.render('index', context, req, 'pages.item')
    return HttpResponse(html)
