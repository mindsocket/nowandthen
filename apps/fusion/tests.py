from django.test import TestCase
from apps.fusion.models import Fusion

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
