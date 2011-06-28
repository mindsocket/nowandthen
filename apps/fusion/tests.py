from django.test import TestCase
from apps.fusion.models import Fusion, ImageAligner
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
        aligner.align("test", outpath='/tmp')

    def test_image_aligner_in_fusion(self):
        """Tests that the image aligner does something useful - ie aligns images"""
        fusion = mockfusion()
        fusion.align()

    @unittest.skip("not needed now")
    def test_pto_generation(self):
        fusion = mockfusion()
        aligner = ImageAligner(fusion)
        print(aligner.get_pto_string())
        
    def _test_page(self, url, string=None):
        response = self.client.get(url)
        if string:
            self.assertContains(response, string, status_code=200)
        else:
            self.assertEqual(response.status_code, 200)
            
    def _login(self):
        response = self.client.post('/account/login/', {'username': 'testuser', 'password': 'test'})
        self.assertEqual(response.status_code, 302)

    def test_homepage(self):
        self._test_page('/', 'Welcome')
        
    def test_fusion_search(self):
        self._test_page('/fusions', "Fusion List")
        
    def test_fusion_feed(self):
        self._test_page('/fusions/rss', "Now and Then Latest Fusions")
        
    def test_image_search(self):
        self._test_page('/images', "Image List")
        
    def test_about(self):
        self._test_page('/about/', 'beer!')
        
    def test_openid_page(self):
        self._test_page("/openid/")
        
    def test_image_view(self):
        self._test_page('/image/view/873/slug', 'viewimage')
        
    def test_fusion_new(self):
        self._login()
        self._test_page('/fusion/new/873/', 'nowandthen tag')
        
    def test_fusion_create(self):
        self._login()
        self._test_page('/fusion/create/873/5518762196/', 'control_point_panel')

    def test_fusion_view(self):
        self._test_page('/fusion/view/1/', 'Fusion by')

    def test_fusion_edit(self):
        self._login()
        self._test_page('/fusion/edit/1/', 'control_point_panel')

    def test_image_map_xml(self):
        self._test_page('/image/map/xml')

    def test_map(self):
        self._test_page('/map', 'map_canvas')

    def test_fusion_latest(self):
        self._test_page('/fusion/latest', 'slideshow')
