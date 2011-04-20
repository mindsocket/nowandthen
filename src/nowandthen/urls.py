from django.conf.urls.defaults import include, patterns
from fusion import views
from django.conf import settings
from django.contrib import admin
from nowandthen.fusion.models import Fusion, Image
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^nowandthen/', include('nowandthen.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # TODO friendly URLs (slugs: add description in URL support)
    (r'^admin/', include(admin.site.urls)),
    (r'^image/add$', views.add_image),
    (r'^social/', include("socialregistration.urls")),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^about/$', TemplateView.as_view(template_name='about.html')),
    (r'^$',  TemplateView.as_view(template_name='index.html')),
)

urlpatterns += patterns('',
    (r'^fusions$', ListView.as_view(queryset=Fusion.objects.all(), paginate_by=20)),
    (r'^images$',  ListView.as_view(queryset=Image.objects.all(),  paginate_by=20)),
    (r'^image/view/(?P<pk>\d+)/.*$', DetailView.as_view(model=Image)),
    (r'^fusion/view/(?P<pk>\d+)/.*$', DetailView.as_view(model=Fusion)),
    (r'^fusion/edit/(?P<pk>\d+)/.*$', UpdateView.as_view(model=Fusion)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
