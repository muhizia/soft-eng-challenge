import json
from django.test import TestCase, Client
from django.urls import reverse, resolve
from military_base.models import MotherShip, Ship, CrewMember
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class TestViews(TestCase):
    
    def setUp(self):
        self.url = '/api/ship/'
        mother = MotherShip.objects.create(id=1, code="x-r")
        Ship.objects.create(mother = mother, id=14, code="x-r-n")
        
    def test_get_hip_ships(self):
        client = APIClient()
        response = client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_ships_by_id(self):
        client = APIClient()
        response = client.get(self.url + '14/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_getShip_ships_by_wrong_id(self):
        client = APIClient()
        response = client.get(self.url + '1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)