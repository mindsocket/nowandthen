from models import Fusion, SourceImage, ImageType, FusionVote, SourceImageVote
from django.contrib import admin

#class SourceImageThenInline(admin.TabularInline):
#    model = SourceImage
#    fk_name = 'then'
#    extra = 0
#
#class SourceImageNowInline(admin.TabularInline):
#    model = SourceImage
#    fk_name = 'now'
#    extra = 0

class FusionVoteInline(admin.TabularInline):
    model = FusionVote
    extra = 0

#class ChallengeAdmin(admin.ModelAdmin):
#    date_hierarchy = 'timestamp'
#    list_display = ('__unicode__', 'ipaddress', 'timestamp')
#    search_fields = ['ipaddress']
#    list_filter = ('timestamp',)

class FusionAdmin(admin.ModelAdmin):
#    list_display = ('fusionname', 'fusionimgimg', 'wincount', 'challengecount')
#    search_fields = ['fusionname']
    inlines = [ FusionVoteInline]
#    def fusionimgimg(self,fusion):
#      img=MediaFile(fusion.fusionimg)
#      thumb=img.thumbnail("64x64gt")
#      return thumb.tag
#    fusionimgimg.allow_tags = True

admin.site.register(Fusion, FusionAdmin)
admin.site.register(FusionVote)
admin.site.register(SourceImage)
admin.site.register(SourceImageVote)
admin.site.register(ImageType)
