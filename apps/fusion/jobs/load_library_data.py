from django_extensions.management.jobs import BaseJob
from django.conf import settings
import csv, codecs
import os
from apps.fusion.models import Image, ImageType, Fusion
from django.db import IntegrityError

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self
    
class Job(BaseJob):
    help = "Data import job for sydney pictures"

    def execute(self):
        Image.objects.filter(type__typename='SYDpre1885').delete()
        f = open(os.path.join(settings.DATA_ROOT, 'NSW', 'sydney-pictures.csv'), 'rb')
        reader = UnicodeReader(f, dialect='excel', encoding='latin1')

        """itemid,title,caption,creator,albumnumber,dateofwork,collectionitemlink,digitalitemlink,digitalordernumber,thumbnaillink,highreslink,zoomablelink,albumorder"""
        """412069,"Sydney - photographs of streets, public buildings, views in the Harbour, suburbs etc., chiefly pre 1885","The City Bank [corner of King & George Streets, Sydney, ca. 1870s]",NULL,412050,[ca. 1870s],http://acms.sl.nsw.gov.au/item/itemdetailpaged.aspx?itemid=412050,http://acms.sl.nsw.gov.au/item/itemdetailpaged.aspx?itemid=412069,a089002,http://acms.sl.nsw.gov.au/_DAMt/image/18/122/a089002t.jpg,http://acms.sl.nsw.gov.au/_DAMx/image/18/122/a089002h.jpg,NULL,1"""
        reader.next()
        lastimage = None
        for row in reader:
            print(row)
            try:
                image, created = Image.objects.get_or_create(type=ImageType.objects.get(typename='SYDpre1885'), 
                                        imageurl=row[10], thumburl=row[9], infourl=row[7],
                                        description=row[2], sourcesystemid=row[8],
                                        creator=row[3], dateofwork=row[5])
            
                if image.id > 1 and image.id < 10:
                    Fusion.objects.get_or_create(then=lastimage, now=image, user_id=1, description="test data")
                
                lastimage = image
            except IntegrityError:
                pass
            
            if image.id > 50:
                break