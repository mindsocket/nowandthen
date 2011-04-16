from django.db import models
from django.contrib import admin
from datetime import datetime
from django.db.models.query import QuerySet

class ImageType(models.Model):
    typename = models.CharField(max_length=32)
    infourl = models.URLField(max_length=256)
    description = models.CharField(max_length=150)
    canbethen = models.BooleanField()

    def __unicode__(self):
        return self.description

class SourceImageQuerySet(QuerySet):
    def topimages(self, limit):
        import logging
        logging.info('Recalculating top images')
        return self.filter(votecount__gte=1).limit(limit).order_by("-votecount") 

class SourceImageManager(models.Manager):
    def get_query_set(self):
        return SourceImageQuerySet(self.model)

    def topimages(self, limit=10):
        return self.get_query_set().topimages(limit)

    def recalculateTotals(self):
        for image in self.all():
            image.votecount=image.vote.count()
            image.save()
    
class SourceImage(models.Model):
    type = models.ForeignKey(ImageType)
    url = models.URLField(max_length=256)
    thumburl = models.URLField(max_length=256)
    description = models.CharField(max_length=150)
    votecount = models.IntegerField(default=0)

    def __unicode__(self):
        return self.description

class SourceImageVote(models.Model):
    image = models.ForeignKey(SourceImage)
    timestamp = models.DateTimeField(default=datetime.now)
    ipaddress = models.IPAddressField()

    def save(self, **kwargs):
        image = SourceImage.objects.get(id=self.image.id)
        image.votecount += 1
        image.save()
        super(SourceImageVote, self).save(**kwargs)

class FusionQuerySet(QuerySet):
    def topfusions(self, limit):
        import logging
        logging.info('Recalculating top fusions')
        return self.filter(votecount__gte=1).limit(limit).order_by("-votecount") 

class FusionManager(models.Manager):
    def get_query_set(self):
        return FusionQuerySet(self.model)

    def topfusions(self, limit=10):
        return self.get_query_set().topfusions(limit)

    def recalculateTotals(self):
        for fusion in self.all():
            fusion.votecount=fusion.vote.count()
            fusion.save()
    
class Fusion(models.Model):
    objects = FusionManager()
    then = models.ForeignKey(SourceImage, related_name='then')
    now = models.ForeignKey(SourceImage, related_name='now')
    usepoints = models.BooleanField()
    description =  models.CharField(max_length=150)
    votecount = models.IntegerField(default=0)

    def __unicode__(self):
        return self.description

    def blend(self):
        return None

class FusionVote(models.Model):
    fusion = models.ForeignKey(Fusion)
    timestamp = models.DateTimeField(default=datetime.now)
    ipaddress = models.IPAddressField()

    def save(self, **kwargs):
        # TODO why did I not just update the fusion object I have? (doesn't work w/ Django's ORM ?)
        fusion = Fusion.objects.get(id=self.fusion.id)
        fusion.votecount += 1
        fusion.save()
        super(FusionVote, self).save(**kwargs)

class ControlPoint(models.Model):
    fusion = models.ForeignKey(Fusion)
    thenx = models.IntegerField()
    theny = models.IntegerField()
    nowx = models.IntegerField()
    nowy = models.IntegerField()

