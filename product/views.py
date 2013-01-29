# Create your views here.
from django.http import HttpResponse
from product.models import Item

# list all products
def list(req):
    items = Item.objects.all()
    res = '<br/>'.join([item.__unicode__() for item in items]);
    return HttpResponse('All products: <br/>' + res)

def product(req, id):
    return HttpResponse('Current product ' + id)
