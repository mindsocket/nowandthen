from django.test import TestCase
from apps.fusion.models import Fusion, Image, ImageAligner
import unittest2 as unittest

def mocknowimage():
    i = Image()
    i.imageurl = "http://nowandthen.mindsocket.com.au/media/cache/fd/fd86c45beed791eda0b5fc50ccbbab71.jpg"
    return i

def mockthenimage():
    i = Image()
    i.imageurl = "http://nowandthen.mindsocket.com.au/media/cache/31/31ec06ffad82a92abd648e46fab54a44.jpg"
    return i

def mockfusion():
    f = Fusion()
    f.id = 999
    f.now = mocknowimage()
    f.then = mockthenimage()
    f.points = "0,0,0,0,100,100,150,150"
    return f

class TestFusion(TestCase):
    """Basic tests for the fusion class"""
    
    def test_point_list(self):
        """Tests that point_list returns a valid list of lists"""
        f = Fusion()
        f.points = "1,2,3,4,5,6,7,8"
        self.failUnlessEqual(f.point_list(), [[1,2,3,4],[5,6,7,8]])

    def test_empty_point_list(self):
        """Tests that point_list returns a valid list of lists"""
        f = Fusion()
        f.points = ""
        self.failUnlessEqual(f.point_list(), [])
        
    def test_image_aligner(self):
        """Tests that the image aligner does something useful - ie aligns images"""
        f = mockfusion()
        a = ImageAligner(f)
        a.align("test")

    @unittest.skip("not needed now")
    def test_pto_generation(self):
        f = mockfusion()
        a = ImageAligner(f)
        print(a.get_pto_string())
