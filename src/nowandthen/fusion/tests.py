from django.test import TestCase
from nowandthen.fusion.models import Fusion, FusionVote

class TestFusion(TestCase):
    """Basic tests for the fusion class"""
    
    def test_point_list(self):
        """Tests that point_list returns a valid list of lists"""
        f = Fusion()
        f.points = "1,2,3,4,5,6,7,8"
        self.failUnlessEqual(f.point_list(), [[1,2,3,4],[5,6,7,8]])

class TestFusionVotes(TestCase):
    def test_new_fusion_vote(self):
        f = Fusion.objects.get(id=1)
        v = FusionVote(fusion=f)
        votesbefore = f.votecount
        self.failUnlessEqual(votesbefore, f.fusionvotes.count())
        v.save()
        f2 = Fusion.objects.get(id=1)
        votesafter = f2.votecount
        self.failUnlessEqual(votesbefore, f2.fusionvotes.count())
        self.failUnlessEqual(votesbefore + 1, votesafter)
        
        
        