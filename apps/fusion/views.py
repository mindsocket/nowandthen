from django.conf import settings
from django.contrib.auth.decorators import login_required
import flickrapi
from django.views.generic.edit import UpdateView, CreateView
from django.core import exceptions, serializers
from apps.fusion.models import Fusion, Image
from django.views.generic.list import ListView
from tagging.models import TaggedItem
from django.contrib.syndication.views import Feed
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from voting.models import Vote
from django.views.generic.simple import direct_to_template, redirect_to
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError, ObjectDoesNotExist
#from django.db.models.query_utils import Q

searchparamslambda = lambda d: '&'.join([k + "=" + d[k] for k in d if k != 'page'])

def send_to_mobile(request):
    return settings.SEND_TO_MOBILE == "always" or (settings.SEND_TO_MOBILE == True and request.is_touch_device)

def HomePage(request):
    template = "mobile_homepage.html" if send_to_mobile(request) else "homepage.html"
    return direct_to_template(request, template)

def TopVotedByUser(request):
    return direct_to_template(request, 'includes/image_table.html', extra_context={ 
            "top_images": Image.objects.in_bulk([v.object_id for v in Vote.objects.filter(user__pk=request.user.id, content_type__pk=ContentType.objects.get(model="image").id)]).values(), "caption":"These are the images you have voted for...", 
        })
    
def ImageMapXML(request):
    data = serializers.serialize('xml', Image.objects.filter(type__canbethen=True, latitude__isnull=False), fields=('description', 'latitude', 'longitude', 'id', 'thumburl'))
    return HttpResponse(data)
    
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

def getFusionQuerySet(request):
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
        
    return queryset

class SearchListView(ListView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SearchListView, self).get_context_data(**kwargs)
        # Add in the searchparams
        context['searchparams'] = searchparamslambda(self.request.GET)
        return context
    
class FusionListView(SearchListView):
    def get(self, request, *args, **kwargs):
        self.queryset = getFusionQuerySet(request)
            
        return super(FusionListView, self).get(request, *args, **kwargs)

class LatestFusionsFeed(Feed):
    title = "Now and Then Latest Fusions"
    link = "/fusions/"
    description = "Latest fusions added to Now and Then"
    absolute_uri = ''

    def get_object(self, request):
        # This ain't pretty on 2 counts:
        # We need the request to build an absolute URL.  This is guaranteed to be called before item_description where it's used
        self.absolute_uri = request.build_absolute_uri('/')[:-1]
        # The request is where all of the fusion search params are, so it become the "object" used by the items method
        return request 
    
    def items(self, obj):
        return getFusionQuerySet(obj).order_by('-timestamp')[:10]

    def item_title(self, item):
        return "A fusion by %s" % item.user

    def item_description(self, item):
        rendered = render_to_string('fusion/fusion_feed_item.html', { 'fusion': item, 'absolute_uri': self.absolute_uri })
        return rendered
    
    def item_link(self, item):
        return reverse('fusion_detail', args=[item.id])

class ImageDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        if send_to_mobile(request):
            self.template_name = 'fusion/mobile_image_detail.html'
        return super(ImageDetailView, self).get(request, *args, **kwargs)

    
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

        if send_to_mobile(request):
            self.template_name = 'fusion/mobile_image_list.html'
            
        return super(ImageListView, self).get(request, *args, **kwargs)
    
def setupFlickr():
    flickr = flickrapi.FlickrAPI(settings.FLICKR_API_KEY, settings.FLICKR_API_SECRET) #, cache=True)
#    flickr.cache = cache
    return flickr

@login_required
def FusionNew(request, thenid):
    thenimg = None
    if thenid:
        thenimg = Image.objects.get(id=thenid)
    
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    myargs = {}
    myargs['page'] = page
    myargs['per_page'] = 15
    #myargs['license'] = '1,2,4,5,7'

    if 'nowandthentag' in request.GET:
        myargs['tags'] = 'nowandthen'
        myargs['tag_mode'] = 'all'

    if 'tag' in request.GET and len(request.GET['tag'].strip()) > 0:
        myargs['tag_mode'] = 'all'
        if 'tags' in myargs:
            myargs['tags'] += ',' + request.GET['tag']
        else: 
            myargs['tags'] = request.GET['tag']

    if 'nowandthengroup' in request.GET or 'init' in request.GET:
        myargs['group_id'] = settings.FLICKR_GROUP_ID
    
    if 'keyword' in request.GET and len(request.GET['keyword'].strip()) > 0:
        myargs['text'] = request.GET['keyword']
    
    flickr = setupFlickr()
    #pylint: disable-msg=W0142
    results = flickr.photos_search(**myargs)

    photosnode = results.find('photos')                
    num_pages = int(photosnode.attrib['pages'])
    page = int(photosnode.attrib['page'])
    photos = photosnode.findall('photo')
    
    return direct_to_template(request, 'fusion/fusion_new.html', extra_context={
        'photos': photos, 'num_pages': num_pages, 'page': page, 'thenid': thenid, 'thenimg': thenimg,
        'searchparams': searchparamslambda(request.GET), 'flickrgroup': settings.FLICKR_GROUP_ID,
        })

def imagefromflickrid(flickrid):
    try:
        now = Image.objects.get(sourcesystemid=flickrid)
    except ObjectDoesNotExist:
        f = setupFlickr()
        result = f.photos_getInfo(photo_id=flickrid)
        photonode=result.find('photo')
        if not photonode.attrib['license'] in ['1','2','4','5','7']:
            raise ValidationError("Image does not have a permissive license") # self.template_name = "image_wrong_license.html"
        now = Image.objects.imageFromFlickrPhoto(photonode)
    return now

@login_required
def FusionFlickrNew(request, flickrid):
    now = imagefromflickrid(flickrid)
    
    return redirect_to(request, '/fusion/new/%d?init=true' % now.id)

class FusionCreateView(CreateView):

    def get_form(self, *args, **kwargs):
        fusion = Fusion()
        fusion.then = Image.objects.get(id=self.kwargs.get('thenid'))
        #pylint: disable-msg=E1101
        flickrid = self.kwargs.get('flickrid')
        now = imagefromflickrid(flickrid)
        fusion.now = now
        fusion.user = self.request.user
        self.object = fusion
        form = super(FusionCreateView, self).get_form(*args, **kwargs)
        return form
