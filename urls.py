from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
from apps.fusion.models import Fusion, FusionForm, Image
from apps.fusion.views import FusionNew, FusionUpdateView, FusionListView,\
    ImageListView, FusionCreateView, LatestFusionsFeed, HomePage, ImageDetailView,\
    ImageMapXML, TopVotedByUser, FusionFlickrNew
from django.views.generic.detail import DetailView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from voting.views import vote_on_object
from django.contrib.auth.decorators import login_required
from pinax.apps.account.openid_consumer import PinaxConsumer
from django.views.generic.simple import direct_to_template
from voting.models import Vote

admin.autodiscover()



handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", HomePage, name="home"),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/(.*)", PinaxConsumer()),
    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
)

#pylint: disable-msg=E1120
urlpatterns += patterns('',
    url(r'^fusions/rss$', LatestFusionsFeed(), name='fusion_feed'),
    url(r'^fusions$', FusionListView.as_view(paginate_by=20), name='fusions'),
    url(r'^images$', ImageListView.as_view(paginate_by=20), name='images'),
    url(r'^image/view/(?P<pk>\d+)/.*$', ImageDetailView.as_view(model=Image), name='image_detail'),
    url(r'^fusion/new/(?P<thenid>\d+)?$', FusionNew, name='fusion_new'),
    url(r'^fusion/flickr_new/(?P<flickrid>\d+)$', FusionFlickrNew, name='fusion_flickr_new'),
    url(r'^fusion/create/(?P<thenid>\d+)/(?P<flickrid>\d+)/.*$', login_required(FusionCreateView.as_view(model=Fusion, form_class=FusionForm, success_url="/fusion/view/%(id)d/")), name='fusion_create'),
    url(r'^fusion/view/(?P<pk>\d+)/.*$', DetailView.as_view(model=Fusion), name='fusion_detail'),
    url(r'^fusion/edit/(?P<pk>\d+)/.*$', FusionUpdateView.as_view(model=Fusion, form_class=FusionForm, owner='user', success_url="/fusion/view/%(id)d/"), name='fusion_form'),
    url(r'^image/map/xml$', ImageMapXML, name='image_map'),
    url(r'^map$', direct_to_template, {'template': "map.html"}, name="map"),
    url(r'^fusion/latest$', direct_to_template, { 'template': 'includes/fusion_latest.html', 'extra_context': { "latest_fusions": lambda: Fusion.objects.all().order_by('-timestamp')[:10], }}, name="fusion_latest"), #IGNORE:E1101
    url(r'^fusion/top$', direct_to_template, { 'template': 'includes/fusion_top.html', 'extra_context': { "top_fusions": lambda: Vote.objects.get_top(Fusion), }}, name="fusion_top"), #IGNORE:E1101
    url(r'^image/top_unfused$', direct_to_template, { 'template': 'includes/image_table.html', 'extra_context': { "top_images": lambda: [image for image, score in Vote.objects.get_top(Image, limit=100) if image.then.count() == 0][:10], "caption":"These images are the top voted historical images that aren't yet part of a fusion...", }}, name="image_top_unfused"), #IGNORE:E1101
    url(r'^image/top_voted$', TopVotedByUser, name="image_voted"), #IGNORE:E1101
)

image_vote_dict = {
    'model': Image,
    'template_object_name': 'image',
    'allow_xmlhttprequest': True,
}

fusion_vote_dict = {
    'model': Fusion,
    'template_object_name': 'fusion',
    'allow_xmlhttprequest': True,
}

urlpatterns += patterns('',
    (r'^image/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', vote_on_object, image_vote_dict),
    (r'^fusion/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', vote_on_object, fusion_vote_dict),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )