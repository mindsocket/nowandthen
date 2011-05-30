from django.shortcuts import get_object_or_404
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
from django.views.generic.edit import UpdateView, CreateView
#from django.views.generic.list import ListView
from django.core import exceptions
from apps.fusion.models import Fusion, Image
from django.views.generic.list import ListView
from tagging.models import TaggedItem

searchparamslambda = lambda d: '&'.join([k + "=" + d[k] for k in d if k != 'page'])

class OwnedUpdateView(UpdateView):
    
    owner = None
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.check_permission(request.user, self.object)
        return super(OwnedUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.check_permission(request.user, self.object)
        return super(OwnedUpdateView, self).post(request, *args, **kwargs)

    def check_permission(self, user, myobject):
        if getattr(myobject, self.owner) != user:
            raise exceptions.PermissionDenied()

class FusionUpdateView(OwnedUpdateView):
    pass
#    def post(self, request, *args, **kwargs):
#        self.object = self.get_object()
#        self.object.align()
#        return super(FusionUpdateView, self).post(request, *args, **kwargs)

class SearchListView(ListView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SearchListView, self).get_context_data(**kwargs)
        # Add in the searchparams
        context['searchparams'] = searchparamslambda(self.request.GET)
        return context
    
class FusionListView(SearchListView):
    def get(self, request, *args, **kwargs):
        myargs = {}
        myargs['publish'] = True
        myargs['hide'] = False

        if 'keyword' in request.GET and len(request.GET['keyword'].strip()) > 0:
            myargs['description__icontains'] = request.GET['keyword']


        if 'justmine' in request.GET:
            myargs['user__id'] = request.user.id

        #pylint: disable-msg=E1101
        #pylint: disable-msg=W0142
        queryset = Fusion.objects.filter(**myargs) 
        
        if 'tag' in request.GET and len(request.GET['tag'].strip()) > 0:
            queryset = TaggedItem.objects.get_by_model(queryset, request.GET['tag'])

        self.queryset = queryset
            
        return super(FusionListView, self).get(request, *args, **kwargs)
    
class ImageListView(SearchListView):
    def get(self, request, *args, **kwargs):
        myargs = {}
        myargs['type__canbethen'] = True
        myargs['hide'] = False

        if 'keyword' in request.GET and len(request.GET['keyword'].strip()) > 0:
            myargs['description__icontains'] = request.GET['keyword']

        #pylint: disable-msg=W0142
        queryset = Image.objects.filter(**myargs) 
        
        if 'tag' in request.GET and len(request.GET['tag'].strip()) > 0:
            queryset = TaggedItem.objects.get_by_model(queryset, request.GET['tag'])

        self.queryset = queryset
            
        return super(ImageListView, self).get(request, *args, **kwargs)
    
def setupFlickr():
    f = flickrapi.FlickrAPI(settings.FLICKR_API_KEY, settings.FLICKR_API_SECRET, cache=True)
    f.cache = cache
    return f

@login_required
def FusionNew(request, thenid):
    thenimg = get_object_or_404(Image, id=thenid)
    
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    myargs = {}
    myargs['page'] = page
    myargs['per_page'] = 15
    myargs['tag_mode'] = 'all'
    myargs['license'] = '1,2,4,5,7'

    if 'nowandthentag' in request.GET or 'init' in request.GET:
        myargs['tags'] = 'nowandthen'

    if 'tag' in request.GET and len(request.GET['tag'].strip()) > 0:
        if 'tags' in myargs:
            myargs['tags'] += ',' + request.GET['tag']
        else: 
            myargs['tags'] = request.GET['tag']

    if 'nowandthengroup' in request.GET:
        myargs['group_id'] = settings.FLICKR_GROUP_ID
    
    if 'keyword' in request.GET and len(request.GET['keyword'].strip()) > 0:
        myargs['text'] = request.GET['keyword']
    
    f = setupFlickr()
    #pylint: disable-msg=W0142
    results = f.photos_search(**myargs)

    photosnode = results.find('photos')                
    num_pages = int(photosnode.attrib['pages'])
    page = int(photosnode.attrib['page'])
    photos = photosnode.findall('photo')
    
    return render_to_response('fusion/fusion_new.html', {
        'photos': photos, 'num_pages': num_pages, 'page': page, 'thenid': thenid, 'thenimg': thenimg,
        'searchparams': searchparamslambda(request.GET), 'flickrgroup': settings.FLICKR_GROUP_ID,
        },
        context_instance=RequestContext(request))

class FusionCreateView(CreateView):

    @login_required    
    def get_form(self, *args, **kwargs):
        fusion = Fusion()
        fusion.then = Image.objects.get(id=self.kwargs.get('thenid'))
        #pylint: disable-msg=E1101
        try:
            now = Image.objects.get(sourcesystemid=self.kwargs.get('flickrid'))
        except Image.DoesNotExist:
            f = setupFlickr()
            result = f.photos_getInfo(photo_id=self.kwargs.get('flickrid'))
            now = Image.objects.imageFromFlickrPhoto(result.find('photo'))
            now.save()
            
        fusion.now = now
        fusion.user = self.request.user
        self.object = fusion
        form = super(FusionCreateView, self).get_form(*args, **kwargs)
        return form
