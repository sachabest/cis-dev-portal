from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import SiteApp

def index(request):
    app_list = SiteApp.objects
    template = loader.get_template('index.html')
    context = {
        'links': app_list
    }
    return HttpResponse(template.render(context, request))