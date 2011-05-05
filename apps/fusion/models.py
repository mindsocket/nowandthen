from django.db import models
from datetime import datetime
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.conf import settings
import subprocess
import tagging
from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput
import tempfile
import os

class ImageType(models.Model):
    typename = models.CharField(max_length=32, unique=True)
    infourl = models.URLField(max_length=256, verify_exists=False, blank=True)
    dataurl = models.URLField(max_length=256, verify_exists=False, blank=True)
    description = models.CharField(max_length=150)
    longdescription = models.CharField(max_length=1024)
    sourcesystemid = models.CharField(max_length=32, editable=False)
    canbethen = models.BooleanField()
    hide = models.BooleanField(default=False)

    def __unicode__(self):
        return self.description

#class ImageQuerySet(QuerySet):
#    def topimages(self, limit):
#        import logging
#        logging.info('Recalculating top images')
#        return self.filter(votecount__gte=1).limit(limit).order_by("-votecount") 
#
#class ImageManager(models.Manager):
#    def get_query_set(self):
#        return ImageQuerySet(self.model)
#
#    def topimages(self, limit=10):
#        return self.get_query_set().topimages(limit)
#
#    def recalculateTotals(self):
#        for image in self.all():
#            image.votecount=image.vote.count()
#            image.save()
    
class Image(models.Model):
#    objects = ImageManager() 
    type = models.ForeignKey(ImageType)
    imageurl = models.URLField(max_length=256, verify_exists=False, unique=True)
    thumburl = models.URLField(max_length=256, verify_exists=False, blank=True)
    infourl = models.URLField(max_length=256, verify_exists=False, blank=True)
    #uploadedimage = models.ImageField(upload_to='uploads')
    description = models.CharField(max_length=150)
#    votecount = models.PositiveIntegerField(default=0, editable=False)
    sourcesystemid = models.CharField(max_length=32, editable=False)
    creator = models.CharField(max_length=32)
    dateofwork = models.CharField(max_length=32)
    hide = models.BooleanField(default=False)

    def __unicode__(self):
        return self.description

#class ImageVote(models.Model):
#    image = models.ForeignKey(Image)
#    timestamp = models.DateTimeField(default=datetime.now)
#    ipaddress = models.IPAddressField()
#
#    def save(self, **kwargs):
#        image = Image.objects.get(id=self.image.id)
#        image.votecount += 1
#        image.save()
#        super(ImageVote, self).save(**kwargs)

#class FusionQuerySet(QuerySet):
#    def topfusions(self, limit):
#        import logging
#        logging.info('Recalculating top fusions')
#        return self.filter(votecount__gte=1).limit(limit).order_by("-votecount") 
#
#class FusionManager(models.Manager):
#    def get_query_set(self):
#        return FusionQuerySet(self.model)
#
#    def topfusions(self, limit=10):
#        return self.get_query_set().topfusions(limit)
#
#    def recalculateTotals(self):
#        for fusion in self.all():
#            fusion.votecount=fusion.vote.count()
#            fusion.save()
    

def get_pto_string(points):
    return """
p f0 w3891 h1946 v50  E0 R0 n"TIFF_m c:LZW"
m g1 i0 f0 m2 p0.00784314
i w3891 h1946 f0 v50.1902546419894 Ra0 Rb0 Rc0 Rd0 Re0 Eev0 Er1 Eb1 r0 p0 y0 TrX0 TrY0 TrZ0 j0 a0 b0 c0 d0 e0 g0 t0 Va1 Vb0 Vc0 Vd0 Vx0 Vy0  Vm5 u10 n"/home/roger/pics/2009/2009_portfolio/night/img_3472_atm.tif.jpg"
i w3891 h1946 f0 v49.1641555686307 Ra=0 Rb=0 Rc=0 Rd=0 Re=0 Eev=0 Er=0 Eb=0 r-0.998287544671579 p0.497171580182977 y0.968101677045995 TrX0 TrY0 TrZ0 j=0 a=0 b=0 c=0 d=0 e=0 g=0 t=0 Va=0 Vb=0 Vc=0 Vd=0 Vx=0 Vy=0  Vm5 u10 n"/home/roger/pics/2009/2009_portfolio/day/img_6713_atm_day.tif.jpg"
v v1 r1 p1 y1
c n0 N1 x3356 y826 X3312 Y884 t0
c n0 N1 x1620.46489104116 y249.664648910412 X1504.14366744986 Y261.372124031008 t0
c n0 N1 x521.996685004461 y232.674665680004 X423.958837772397 Y221.400726392252 t0
"""

def split_pointstring(points, howmany=4):
    if len(points) < howmany:
        return []
    pointlist = [int(point) for point in points.split(',')]
    return [pointlist[start:start + howmany] for start in range(0, len(points.split(',')), howmany)]

class Fusion(models.Model):
#    objects = FusionManager()
    then = models.ForeignKey(Image, related_name='then', limit_choices_to={'type__canbethen': True})
    now = models.ForeignKey(Image, related_name='now')
    user = models.ForeignKey(User, related_name='+')
    points = models.CommaSeparatedIntegerField(max_length=512, blank=True)
    cropthen = models.CommaSeparatedIntegerField(max_length=20, blank=True)
    publish = models.BooleanField(default=True)
    description =  models.CharField(max_length=150, blank=True)
#    votecount = models.PositiveIntegerField(default=0, editable=False)
    hide = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)

    def __unicode__(self):
        return self.description

    def align(self):
        pto_string = get_pto_string(self.point_list())
        fd, pto_file = tempfile.mkstemp(suffix='.pto')
        
        proc = subprocess.Popen(['autooptimiser', '-a', '-o %s' % file, '-'],
                        stdin=subprocess.PIPE,
                        )
        proc.communicate(pto_string)
        
        subprocess.call(['nona', '-r ldr', '-m JPEG', '-o', os.path.join(settings.MEDIA_ROOT, self.aligned_filename('then')), '-i 0', pto_file])
        subprocess.call(['nona', '-r ldr', '-m JPEG', '-o', os.path.join(settings.MEDIA_ROOT, self.aligned_filename('now')), '-i 1', pto_file])
        os.unlink(pto_file)
    
    def point_list(self):
        return split_pointstring(self.points)
    
    def aligned_filename(self, align_type):
        return os.path.join('fusions', '%i.%s.jpg' % (self.id, align_type))
    
    def get_absolute_url(self):
        return "/fusion/edit/%i/" % self.id

class FusionForm(ModelForm):
    
    class Meta:
        model = Fusion
        
        fields = ('points', 'cropthen', 'publish', 'description')
        widgets = {
            'points': HiddenInput,
            'cropthen': HiddenInput,
        }
#tagging.register(ImageType)
#tagging.register(Image)
#tagging.register(Fusion)
