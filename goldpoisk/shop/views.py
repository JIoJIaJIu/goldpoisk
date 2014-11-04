# Create your views here.
from django.http import HttpResponse

def list(req):
    return HttpResponse('All shops')

def shop(req, id):
    return HttpResponse('Current shop ' + id)
