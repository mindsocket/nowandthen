from django.test import TestCase
from apps.fusion.models import Fusion, Image, ImageAligner
import unittest2 as unittest

def mocknowimage():
    image = Image()
    image.imageurl = "http://nowandthen.mindsocket.com.au/media/cache/fd/fd86c45beed791eda0b5fc50ccbbab71.jpg"
    return image

def mockthenimage():
    image = Image()
    image.imageurl = "http://nowandthen.mindsocket.com.au/media/cache/31/31ec06ffad82a92abd648e46fab54a44.jpg"
    return image

def mockfusion():
    fusion = Fusion()
    fusion.id = 999
    fusion.now = mocknowimage()
    fusion.then = mockthenimage()
    fusion.points = "0,0,0,0,100,100,150,150"
    return fusion

class TestFusion(TestCase):
    """Basic tests for the fusion class"""
    
    def test_point_list(self):
        """Tests that point_list returns a valid list of lists"""
        fusion = Fusion()
        fusion.points = "1,2,3,4,5,6,7,8"
        self.failUnlessEqual(fusion.point_list(), [[1,2,3,4],[5,6,7,8]])

    def test_empty_point_list(self):
        """Tests that point_list returns a valid list of lists"""
        fusion = Fusion()
        fusion.points = ""
        self.failUnlessEqual(fusion.point_list(), [])
        
    def test_image_aligner(self):
        """Tests that the image aligner does something useful - ie aligns images"""
        fusion = mockfusion()
        aligner = ImageAligner(fusion)
        aligner.align("test")

    def test_image_aligner_in_fusion(self):
        """Tests that the image aligner does something useful - ie aligns images"""
        fusion = mockfusion()
        fusion.align()

    @unittest.skip("not needed now")
    def test_pto_generation(self):
        fusion = mockfusion()
        aligner = ImageAligner(fusion)
        print(aligner.get_pto_string())

