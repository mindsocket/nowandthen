from models import Fusion, Image, ImageType
from django.contrib import admin
from convert.base import MediaFile
from django.conf import settings

class FusionThenInline(admin.TabularInline):
    model = Fusion
    fk_name = 'then'
    extra = 0

class FusionNowInline(admin.TabularInline):
    model = Fusion
    fk_name = 'now'
    extra = 0

class ImageInline(admin.TabularInline):
    model = Image
    fk_name = 'type'
    fields = ('description', 'latitude', 'longitude')
    extra = 0
    def geotext(self, fusion):
        return fusion.description

def thumbimg(image):
    img=MediaFile(image.thumburl)
    try:
        tag = img.tag
    except IOError:
        tag = "<font color=\"red\">Bad link!</font>"
    return tag

class FusionAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ('__unicode__', 'thenthumb', 'nowthumb', 'user', 'timestamp')
    list_filter = ('timestamp',)

    def thenthumb(self,fusion):
        return thumbimg(fusion.then)
    thenthumb.allow_tags = True

    def nowthumb(self,fusion):
        return thumbimg(fusion.now)
    nowthumb.allow_tags = True

class ImageTypeAdmin(admin.ModelAdmin):
    inlines = [ ImageInline, ]
    
class ImageAdmin(admin.ModelAdmin):
    list_display = ('type', 'thumbimg', 'imageurl', 'infourl', 'description', 'creator', 'dateofwork', 'hide', 'latitude', 'longitude', 'tags', 'map')
    search_fields = ['description']
    inlines = [ FusionThenInline, FusionNowInline, ]

    def thumbimg(self,image):
        return thumbimg(image)
    thumbimg.allow_tags = True
    
    def map(self,image):
        if not image.latitude:
            return ''
        return '<img src="http://maps.google.com/maps/api/staticmap?center=%f,%f&size=150x150&zoom=14&sensor=false">' % (image.latitude, image.longitude) 
    map.allow_tags = True
                
admin.site.register(Fusion, FusionAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(ImageType, ImageTypeAdmin)
