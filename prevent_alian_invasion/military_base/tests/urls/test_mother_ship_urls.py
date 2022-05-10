from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from military_base.views.mothership_views import  getMotherShips, createMotherShip, getMotherShipById, updateMotherShip, deleteMotherShip

# Create your tests here.

class TestUrls(SimpleTestCase):
    
    def test_motherships_url_is_resolved(self):
        url = reverse('motherships')
        self.assertEqual(resolve(url).func, getMotherShips)
    
    def test_mothership_create_url_is_resolved(self):
        url = reverse('mothership_create')
        self.assertEqual(resolve(url).func, createMotherShip)
        
    def test_mothership_id_url_is_resolved(self):
        url = reverse('mothership_id', args=['id'])
        self.assertEqual(resolve(url).func, getMotherShipById)
        
    def test_mothership_update_url_is_resolved(self):
        url = reverse('mothership_update', args=['id'])
        self.assertEqual(resolve(url).func, updateMotherShip)
    
    def test_mothership_delete_url_is_resolved(self):
        url = reverse('mothership_delete', args=['id'])
        self.assertEqual(resolve(url).func, deleteMotherShip)    