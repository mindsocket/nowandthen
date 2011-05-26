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
from convert.base import MediaFile
import PIL

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

class ImageAligner:
    
    def __init__(self, fusion):
        self.fusion = fusion
    
    def get_pto_string(self):
        pointlist = self.fusion.point_list()
#        import pdb; pdb.set_trace()
        then = MediaFile(self.fusion.then.imageurl)
        now = MediaFile(self.fusion.now.imageurl)
        print(pointlist)
        print(then.path)
        print(now.path)
        
        then_image = PIL.Image.open(then.path)
        now_image = PIL.Image.open(now.path)
        pto_string = 'p f0 w%i h%i v10  E1 R0 n"JPEG"\n' % then_image.size
        pto_string += 'm i0\n'
        pto_string += 'i w%i h%i f0 v10 Eev1 Er1 Eb1 r0 p0 y0 TrX0 TrY0 TrZ0 j0 g0 t0 u10 n"%s"\n' % (then_image.size[0], then_image.size[1], then.path)
        pto_string += 'i w%i h%i f0 v10 Eev1 Er1 Eb1 r0 p0 y0 TrX0 TrY0 TrZ0 j0 g0 t0 u10 n"%s"\n' % (now_image.size[0], now_image.size[1], now.path)
        pto_string += 'v v1 r1 p1 y1\n'
        for pointset in pointlist: 
            pto_string += 'c n0 N1 x%i y%i X%i Y%i t0\n' % tuple(pointset)

        return pto_string

    def align(self, fileprefix, outpath=settings.MEDIA_ROOT):
        pto_string = self.get_pto_string()
        fd, pto_file = tempfile.mkstemp(suffix='.pto')
        
        myfile = os.fdopen(fd, "w")
        myfile.write(pto_string)
        myfile.flush()
        myfile.close()
        
        fd, pto_file2 = tempfile.mkstemp(suffix='.pto')
        subprocess.call(['autooptimiser', '-n', '-o', pto_file2, pto_file])
        thenfile = os.path.join(outpath, fileprefix + '_then')
        nona_command = 'nona -r ldr -i 0 -o %s %s' % (thenfile, pto_file2)
        subprocess.call(nona_command, shell=True)
        nowfile = os.path.join(outpath, fileprefix + '_now')
        nona_command = 'nona -r ldr -i 1 -o %s %s' % (nowfile, pto_file2)
        subprocess.call(nona_command, shell=True)
        os.unlink(pto_file)
        os.unlink(pto_file2)
        return thenfile, nowfile

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
    hide = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    thenfile = models.FilePathField(path=os.path.join(settings.MEDIA_ROOT, 'fusions'), blank=True, null=True)
    nowfile = models.FilePathField(path=os.path.join(settings.MEDIA_ROOT, 'fusions'), blank=True, null=True)
    
    def __unicode__(self):
        return self.description

    def align(self):
        aligner = ImageAligner(self)
        thenfile, nowfile = aligner.align(self.aligned_filename())
        self.thenfile = str(self.id) + '_then.jpg'
        self.nowfile = str(self.id) + '_now.jpg'
    
    def point_list(self):
        return split_pointstring(self.points)
    
    def aligned_filename(self):
        return os.path.join('fusions', str(self.id))
    
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
try:        
    tagging.register(ImageType)
except tagging.AlreadyRegistered:
    pass

try:
    tagging.register(Image)
except tagging.AlreadyRegistered:
    pass

try:
    tagging.register(Fusion)
except tagging.AlreadyRegistered:
    pass

