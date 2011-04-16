from django.conf.urls.defaults import include, patterns
from django.contrib import admin
from fusion import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^nowandthen/', include('nowandthen.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^about/$', views.about),
    (r'^auth/', include("socialregistration.urls"))
)
