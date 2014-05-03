# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.db.models import Min, Max
from product.models import Item, Product

# list all products
def list(req):
    products = Product.objects.annotate(min_cost=Min('item__cost'), max_cost=Max('item__cost'))

    template = loader.get_template('pages/products/list.tmpl')
    c = Context({
        'products': products
    })
    res = HttpResponse(template.render(c))
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
