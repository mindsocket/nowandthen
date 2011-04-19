from django.conf.urls.defaults import include, patterns
from fusion import views
from django.conf import settings
from django.contrib import admin
from nowandthen.fusion.models import Fusion, Image
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^nowandthen/', include('nowandthen.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # TODO friendly URLs (slugs: add description in URL support)
    (r'^admin/', include(admin.site.urls)),
    (r'^image/view/(?P<id>.*)$', views.view_image),
    (r'^image/add$', views.add_image),
    (r'^fusion/view/(?P<id>.*)$', views.view_fusion),
    (r'^fusion/edit/(?P<id>.*)$', views.edit_fusion),
    (r'^auth/', include("socialregistration.urls")),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^about/$',   'direct_to_template', {'template': 'about.html'}),
    (r'^$',         'direct_to_template', {'template': 'index.html'}),
)

urlpatterns += patterns('django.views.generic.list_detail',
    (r'^fusions$',   'object_list', {'queryset': Fusion.objects.all(), 'paginate_by': 20}),
    (r'^images$',    'object_list', {'queryset': Image.objects.all(), 'paginate_by': 20}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
