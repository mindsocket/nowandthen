from django.db import models
from django.contrib.auth.models import User
from apps.fusion.tokenizer import extract_words
from django.conf import settings
import subprocess
import tagging
from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput
import tempfile
import os
from convert.base import MediaFile
import PIL
from tagging.models import Tag
from datetime import datetime
import urllib
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

class ImageType(models.Model):
    typename = models.CharField(max_length=32, unique=True)
    infourl = models.URLField(max_length=255, verify_exists=False, blank=True)
    dataurl = models.URLField(max_length=255, verify_exists=False, blank=True)
    description = models.CharField(max_length=150)
    longdescription = models.CharField(max_length=1024)
    sourcesystemid = models.CharField(max_length=32, editable=False)
    canbethen = models.BooleanField()
    hide = models.BooleanField(default=False)

    def __unicode__(self):
        return self.description

class ImageManager(models.Manager):
    def imageFromFlickrPhoto(self, photonode):
        image = Image()
        #pylint: disable-msg=E1101
        image.type = ImageType.objects.get(typename='flickr')
        urlbase = "http://farm%s.static.flickr.com/%s/%s_%s" % ( 
            photonode.attrib['farm'],
            photonode.attrib['server'],
            photonode.attrib['id'],
            photonode.attrib['secret'],
            )
        image.imageurl = urlbase + "_b.jpg"
        image.thumburl = urlbase + "_t.jpg"
        image.infourl = photonode.find('urls').find('url').text
        image.description = photonode.find('title').text
        image.sourcesystemid = photonode.attrib['id']
        image.creator = photonode.find('owner').attrib['username']
        image.dateofwork = photonode.find('dates').attrib['taken']
        try: 
            image.latitude = float(photonode.find('location').attrib['latitude'])
            image.longitude = float(photonode.find('location').attrib['longitude'])
        except AttributeError:
            pass
        image.save()
        try: 
            tagnodes = photonode.find('tags').findall('tag')
            image.tags = ','.join([tagnode.text for tagnode in tagnodes])
        except AttributeError:
            pass
        return image
    
class Image(models.Model):
    objects = ImageManager() 
    type = models.ForeignKey(ImageType, related_name='type')
    imageurl = models.URLField(max_length=255, verify_exists=False, unique=True)
    thumburl = models.URLField(max_length=255, verify_exists=False, blank=True)
    infourl = models.URLField(max_length=255, verify_exists=False, blank=True)
    description = models.CharField(max_length=150)
    sourcesystemid = models.CharField(max_length=32, editable=False)
    creator = models.CharField(max_length=32)
    dateofwork = models.CharField(max_length=32)
    hide = models.BooleanField(default=False)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
  
    def __unicode__(self):
        return self.description
    
class ImageAligner:
    
    def __init__(self, fusion):
        self.fusion = fusion
    
    def get_pto_string(self):
        pointlist = self.fusion.point_list()
        then = MediaFile(self.fusion.then.imageurl)
        now = MediaFile(self.fusion.now.imageurl)
        
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
        import logging
        logging.info("Aligning fusion " + str(self.fusion.id))
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
    timestamp = models.DateTimeField(default=datetime.now)
        
    def __unicode__(self):
        return self.description

    def align(self):
        #pylint: disable-msg=E1101
        aligner = ImageAligner(self)
        #thenfile, nowfile = 
        aligner.align(self.aligned_filename())
        self.thenfile = 'fusions/' + str(self.id) + '_then.jpg'
        self.nowfile = 'fusions/' + str(self.id) + '_now.jpg'
    
    def point_list(self):
        return split_pointstring(self.points)
    
    def aligned_filename(self):
        #pylint: disable-msg=E1101
        return os.path.join('fusions', str(self.id))
    
    def get_absolute_url(self):
        #pylint: disable-msg=E1101
        return "/fusion/edit/%i/" % self.id
    
    def latitude(self):
        return self.now.latitude if self.now.latitude else self.then.latitude 
    
    def longitude(self):
        return self.now.longitude if self.now.longitude else self.then.longitude
        
class FusionForm(ModelForm):
    
    class Meta: #IGNORE:W0232
        model = Fusion
        
        fields = ('points', 'cropthen')
        widgets = {
            'points': HiddenInput,
            'cropthen': HiddenInput,
        }

    def save(self, *args, **kwargs):
        fusion = super(FusionForm, self).save(*args, **kwargs)
        import logging
        logging.info("Saved fusion " + str(fusion.id) + " by " + fusion.user.username)

        if len(fusion.points) > 4:
            fusion.align()
        
        Tag.objects.update_tags(fusion, ','.join([tag.name for tag in fusion.then.tags] + extract_words(fusion.now.description))) 
        fusion.save()
        return fusion

def get_lat_long(location):
    key = settings.GOOGLE_API_KEY
    output = "csv"
    location = urllib.quote_plus(location)
    request = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % (location, output, key)
    data = urllib.urlopen(request).read()
    dlist = data.split(',')
    if dlist[0] == '200':
        # TODO return accuracy too
        return "%s, %s" % (dlist[2], dlist[3])
    else:
        return ''
        
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

