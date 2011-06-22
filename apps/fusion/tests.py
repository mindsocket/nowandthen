from django.test import TestCase
from apps.fusion.models import Fusion, Image, ImageAligner
import unittest2 as unittest

def mockfusion():
    return Fusion.objects.get(id=999)

class TestFusion(TestCase):
    """Basic tests for the fusion class"""
    fixtures = ['tests.json', 'initial_data.json']
        
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

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_fusion_search(self):
        response = self.client.get('/fusions')
        self.assertEqual(response.status_code, 200)
        
    def test_fusion_feed(self):
        response = self.client.get('/fusions/rss')
        self.assertEqual(response.status_code, 200)
        
    def test_image_search(self):
        response = self.client.get('/images')
        self.assertEqual(response.status_code, 200)
        
    def test_mobile_image_search(self):
        response = self.client.get('/mobile/images')
        self.assertEqual(response.status_code, 200)
                