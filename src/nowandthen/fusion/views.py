from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from models import Image, Fusion
from django.core.paginator import Paginator, InvalidPage, EmptyPage
#from django.core.cache import cache
#from django.http import Http404
#import logging
#from django.conf import settings
from django.contrib.auth.decorators import login_required
#from django.views.decorators.cache import cache_page

def get_paginator(request, object_list, per_page=20):
    paginator = Paginator(object_list, per_page)
# Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
# If page request (9999) is out of range, deliver last page of results.
    try:
        paginated_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        paginated_list = paginator.page(paginator.num_pages)
    return paginated_list

def view_image(request, id):
    image = get_object_or_404(Image, id=id)
    return render_to_response('view_image.html', {'image': image},
        context_instance=RequestContext(request))

@login_required
def add_image(request):
    return render_to_response('add_image.html',
        context_instance=RequestContext(request))

def view_fusion(request, id):
    fusion = get_object_or_404(Fusion, id=id)
    return render_to_response('view_fusion.html', {'fusion': fusion},
        context_instance=RequestContext(request))

@login_required
def edit_fusion(request, id):
    try: 
        int(id)
        fusion = get_object_or_404(Fusion, id=id)
    except ValueError:
        fusion = Fusion()

    return render_to_response('edit_fusion.html', {'fusion': fusion},
        context_instance=RequestContext(request))



