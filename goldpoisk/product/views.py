import copy
import os
from PyV8 import JSArray
from pybem import pybem

from django.http import HttpResponse, Http404
from django.db.models import Min, Max

from goldpoisk import settings
from goldpoisk.product.models import Item, Product
from goldpoisk.templates import get_with_active_menu

renderer = pybem.BEMRender(os.path.abspath(settings.TEMPLATE_DIRS[0]))

def category(req, category):
    html = renderer.render('index', {
        'menu': JSArray(get_with_active_menu(category)),
    }, req, 'blocks.page')

    res = HttpResponse(html)
    return res

def product(req, id):
    try:
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        raise Http404

    template = loader.get_template('pages/products/item.tmpl')
    c = Context({
        'product': product
    })
    return HttpResponse(template.render(c))
