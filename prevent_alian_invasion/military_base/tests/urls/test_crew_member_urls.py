from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from military_base.views.crew_member_views import  getCrewMembers, createCrewMember, getCrewMemberById, updateCrewMember, moveCrewMember, deleteCrewMember

# Create your tests here.

class TestUrls(SimpleTestCase):
    
    def test_crewmembers_url_is_resolved(self):
        url = reverse('crewmembers')
        self.assertEqual(resolve(url).func, getCrewMembers)
    
    def test_crewmember_create_url_is_resolved(self):
        url = reverse('crewmember_create')
        self.assertEqual(resolve(url).func, createCrewMember)
        
    def test_crewmember_id_url_is_resolved(self):
        url = reverse('crewmember_id', args=['id'])
        self.assertEqual(resolve(url).func, getCrewMemberById)
        
    def test_crewmember_update_url_is_resolved(self):
        url = reverse('crewmember_update', args=['id'])
        self.assertEqual(resolve(url).func, updateCrewMember)
        
    def test_crewmember_move_url_is_resolved(self):
        url = reverse('crewmember_move', args=['id'])
        self.assertEqual(resolve(url).func, moveCrewMember)
    
    def test_crewmember_delete_url_is_resolved(self):
        url = reverse('crewmember_delete', args=['id'])
        self.assertEqual(resolve(url).func, deleteCrewMember)    