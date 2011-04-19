from django_extensions.management.jobs import BaseJob
from django.conf import settings
import csv
import os
from nowandthen.fusion.models import Image, ImageType

class Job(BaseJob):
    help = "Data import job for sydney pictures"

    def execute(self):
        Image.objects.filter(type__typename='SYDpre1885').delete()
        reader = csv.reader(open(os.path.join(settings.DATA_ROOT,'NSW','sydney-pictures.csv'), 'rb'), dialect='excel')
           
        """itemid,title,caption,creator,albumnumber,dateofwork,collectionitemlink,digitalitemlink,digitalordernumber,thumbnaillink,highreslink,zoomablelink,albumorder"""
        """412069,"Sydney - photographs of streets, public buildings, views in the Harbour, suburbs etc., chiefly pre 1885","The City Bank [corner of King & George Streets, Sydney, ca. 1870s]",NULL,412050,[ca. 1870s],http://acms.sl.nsw.gov.au/item/itemdetailpaged.aspx?itemid=412050,http://acms.sl.nsw.gov.au/item/itemdetailpaged.aspx?itemid=412069,a089002,http://acms.sl.nsw.gov.au/_DAMt/image/18/122/a089002t.jpg,http://acms.sl.nsw.gov.au/_DAMx/image/18/122/a089002h.jpg,NULL,1"""
        reader.next()
        for row in reader:
            Image.objects.get_or_create(type=ImageType.objects.get(typename='SYDpre1885'), 
                                        imageurl=row[10], thumburl=row[9], infourl=row[7],
                                        description=row[2], sourcesystemid=row[8],
                                        creator=row[3], dateofwork=row[5],
                                        keywords='')
            break



