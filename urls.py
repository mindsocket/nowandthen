from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
from apps.fusion.models import Fusion, FusionForm, Image
from apps.fusion.views import FusionNew, FusionUpdateView, FusionListView,\
    ImageListView, FusionCreateView, LatestFusionsFeed, HomePage, ImageDetailView
from django.views.generic.detail import DetailView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from voting.views import vote_on_object
from django.contrib.auth.decorators import login_required
from pinax.apps.account.openid_consumer import PinaxConsumer

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
    url(r'^fusion/new/(?P<thenid>\d+)/.*$', FusionNew, name='fusion_new'),
    url(r'^fusion/create/(?P<thenid>\d+)/(?P<flickrid>\d+)/.*$', login_required(FusionCreateView.as_view(model=Fusion, form_class=FusionForm, success_url="/fusion/view/%(id)d/")), name='fusion_create'),
    url(r'^fusion/view/(?P<pk>\d+)/.*$', DetailView.as_view(model=Fusion), name='fusion_detail'),
    url(r'^fusion/edit/(?P<pk>\d+)/.*$', FusionUpdateView.as_view(model=Fusion, form_class=FusionForm, owner='user', success_url="/fusion/view/%(id)d/"), name='fusion_form'),
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