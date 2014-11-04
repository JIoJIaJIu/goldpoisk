from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.template import Context, loader

def admin(req):
    if not req.user.is_authenticated():
        return HttpResponseRedirect('login')

    return HttpResponse('Ok');

def login(req):
    if req.method.POST:
        user = login(req)
        raise Http404()

    template = loader.get_template('login.html')
    c = Context({
        'form': AuthenticationForm
    })

    return HttpResponse(template.render(c))
