from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
from apps.fusion.models import Fusion, FusionForm, Image
from apps.fusion.views import add_image, FusionUpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/(.*)", PinaxConsumer()),
    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
)

urlpatterns += patterns('',
    (r'^fusions$', ListView.as_view(queryset=Fusion.objects.all(), paginate_by=20)),
    (r'^images$',  ListView.as_view(queryset=Image.objects.all(), paginate_by=20)),
    (r'^image/view/(?P<pk>\d+)/.*$', DetailView.as_view(model=Image)),
    (r'^image/add/', add_image),
    (r'^fusion/view/(?P<pk>\d+)/.*$', DetailView.as_view(model=Fusion)),
    (r'^fusion/edit/(?P<pk>\d+)/.*$', FusionUpdateView.as_view(model=Fusion, form_class=FusionForm, owner='user', success_url="/fusion/view/%(id)d/")),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )