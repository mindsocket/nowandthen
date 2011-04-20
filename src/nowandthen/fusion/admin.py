from models import Fusion, Image, ImageType
from django.contrib import admin
from convert.base import MediaFile

#class ChallengeAdmin(admin.ModelAdmin):
#    date_hierarchy = 'timestamp'
#    list_display = ('__unicode__', 'ipaddress', 'timestamp')
#    search_fields = ['ipaddress']
#    list_filter = ('timestamp',)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('type', 'thumbimg', 'imageurl', 'infourl', 'description', 'creator', 'dateofwork', 'hide')
    search_fields = ['fusionname']

    def thumbimg(self,image):
        img=MediaFile(image.thumburl)
        #      thumb=img.thumbnail("64x64gt")
        try:
            tag = img.tag
        except IOError:
            tag = "<font color=\"red\">Bad link!</font>"
        return tag
    thumbimg.allow_tags = True

admin.site.register(Fusion)
admin.site.register(Image, ImageAdmin)
admin.site.register(ImageType)
