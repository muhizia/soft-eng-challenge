from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from military_base.views.ship_views import  getShips, createShip, getShipById, updateShip, deleteShip

# Create your tests here.

class TestUrls(SimpleTestCase):
    
    def test_ships_url_is_resolved(self):
        url = reverse('ships')
        self.assertEqual(resolve(url).func, getShips)
    
    def test_ship_create_url_is_resolved(self):
        url = reverse('ship_create')
        self.assertEqual(resolve(url).func, createShip)
        
    def test_ship_id_url_is_resolved(self):
        url = reverse('ship_id', args=['id'])
        self.assertEqual(resolve(url).func, getShipById)
        
    def test_ship_update_url_is_resolved(self):
        url = reverse('ship_update', args=['id'])
        self.assertEqual(resolve(url).func, updateShip)
    
    def test_ship_delete_url_is_resolved(self):
        url = reverse('ship_delete', args=['id'])
        self.assertEqual(resolve(url).func, deleteShip)    