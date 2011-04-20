from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from models import Image, Fusion
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.cache import cache
#from django.http import Http404
import logging
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import flickrapi
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

def require_flickr_auth(view):
    '''View decorator, redirects users to Flickr when no valid
    authentication token is available.
    '''

    def protected_view(request, *args, **kwargs):
        if 'token' in request.session:
            token = request.session['token']
            logging.info('Getting token from session: %s' % token)
        else:
            token = None
            logging.info('No token in session')

        f = flickrapi.FlickrAPI(settings.FLICKR_API_KEY,
               settings.FLICKR_API_SECRET, token=token,
               store_token=False)

        if token:
            # We have a token, but it might not be valid
            logging.info('Verifying token')
            try:
                f.auth_checkToken()
            except flickrapi.FlickrError:
                token = None
                del request.session['token']

        if not token:
            # No valid token, so redirect to Flickr
            logging.info('Redirecting user to Flickr to get frob')
            url = f.web_login_url(perms='read')
            return HttpResponseRedirect(url)

        # If the token is valid, we can call the decorated view.
        logging.info('Token is valid')

        return view(request, *args, **kwargs)

    return protected_view

def callback(request):
    logging.info('We got a callback from Flickr, store the token')

    f = flickrapi.FlickrAPI(settings.FLICKR_API_KEY,
           settings.FLICKR_API_SECRET, store_token=False)

    frob = request.GET['frob']
    token = f.get_token(frob)
    request.session['token'] = token

    return HttpResponseRedirect('/content')
    
@require_flickr_auth
def add_image(request):
    f = flickrapi.FlickrAPI(settings.FLICKR_API_KEY, settings.FLICKR_API_SECRET, 
                            token=request.session['token'], store_token=False, cache=True)
    f.cache = cache
    
#    for photo in f.walk(tag_mode='all',
#        tags='sybren,365,threesixtyfive',
#        min_taken_date='2008-08-20',
#        max_taken_date='2008-08-30'):
#    print photo.get('title')
        
    return render_to_response('add_image.html',
        context_instance=RequestContext(request))

def view_fusion(request, id):
    fusion = get_object_or_404(Fusion, id=id)
    return render_to_response('view_fusion.html', {'fusion': fusion},
        context_instance=RequestContext(request))

#@require_flickr_auth
def edit_fusion(request, id):
    try: 
        int(id)
        fusion = get_object_or_404(Fusion, id=id)
    except ValueError:
        fusion = Fusion()

    return render_to_response('edit_fusion.html', {'fusion': fusion},
        context_instance=RequestContext(request))

