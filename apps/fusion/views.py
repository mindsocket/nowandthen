#from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
#from models import Image, Fusion
#from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.cache import cache
#from django.http import Http404
#import logging
from django.conf import settings
from django.contrib.auth.decorators import login_required
#from django.http import HttpResponseRedirect
import flickrapi
#from apps.fusion.models import FusionForm
#from django.views.decorators.cache import cache_page
#from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
#from django.views.generic.list import ListView
from django.core import exceptions
from apps.fusion.models import ImageAligner
#from django.core.exceptions import ImproperlyConfigured
#from django.http import Http404, HttpResponseRedirect

#def require_flickr_auth(view):
#    '''View decorator, redirects users to Flickr when no valid
#    authentication token is available.
#    '''
#
#    def protected_view(request, *args, **kwargs):
#        if 'token' in request.session:
#            token = request.session['token']
#            logging.info('Getting token from session: %s' % token)
#        else:
#            token = None
#            logging.info('No token in session')
#
#        f = flickrapi.FlickrAPI(settings.FLICKR_API_KEY,
#               settings.FLICKR_API_SECRET, token=token,
#               store_token=False)
#
#        if token:
#            # We have a token, but it might not be valid
#            logging.info('Verifying token')
#            try:
#                f.auth_checkToken()
#            except flickrapi.FlickrError:
#                token = None
#                del request.session['token']
#
#        if not token:
#            # No valid token, so redirect to Flickr
#            logging.info('Redirecting user to Flickr to get frob')
#            url = f.web_login_url(perms='read')
#            return HttpResponseRedirect(url)
#
#        # If the token is valid, we can call the decorated view.
#        logging.info('Token is valid')
#
#        return view(request, *args, **kwargs)
#
#    return protected_view
#
#def callback(request):
#    logging.info('We got a callback from Flickr, store the token')
#
#    f = flickrapi.FlickrAPI(settings.FLICKR_API_KEY,
#           settings.FLICKR_API_SECRET, store_token=False)
#
#    frob = request.GET['frob']
#    token = f.get_token(frob)
#    request.session['token'] = token
#
#    return HttpResponseRedirect('/content')

#class GuardedDetailView(DetailView):
#    def get(self, request, **kwargs):
#        self.object = self.get_object()
#        self.check_permission(request.user, self.object)
#        context = self.get_context_data(object=self.object)
#        return self.render_to_response(context)

class OwnedUpdateView(UpdateView):
    
    owner = None
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.check_permission(request.user, self.object)
        return super(UpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.check_permission(request.user, self.object)
        return super(UpdateView, self).post(request, *args, **kwargs)

    def check_permission(self, user, object):
        if getattr(object, self.owner) != user:
            raise exceptions.PermissionDenied()

class FusionUpdateView(OwnedUpdateView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.align()
        return super(OwnedUpdateView, self).post(request, *args, **kwargs)
    
@login_required
def add_image(request):
    f = flickrapi.FlickrAPI(settings.FLICKR_API_KEY, settings.FLICKR_API_SECRET, cache=True)
    f.cache = cache
    results = f.walk(tag_mode='all', tags='nowandthen', license='1,2,4,5,7', media='photos')
    #group_id ?
    photos=[]
    for photo in results:
        photos.add({'title':"foo", 'photo':photo})
            
    return render_to_response('fusion/image_add.html', {'results': results, 'photos': photos},
        context_instance=RequestContext(request))
