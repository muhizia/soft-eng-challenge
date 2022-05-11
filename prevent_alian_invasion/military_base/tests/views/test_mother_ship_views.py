import json
from django.test import TestCase, Client
from django.urls import reverse, resolve
from military_base.models import MotherShip, Ship, CrewMember
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class TestViews(TestCase):
    
    def setUp(self):
        self.url = '/api/mothership/'
        MotherShip.objects.create(id=14, code="x-r")
        # Opening JSON file
        f = open('/Users/muhizi/Documents/fulgel/soft-eng-challenge/json.json')
        self.data = json.load(f)
    
    
    def test_get_mother_ships(self):
        client = APIClient()
        response = client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_mother_ships_by_id(self):
        client = APIClient()
        response = client.get(self.url + '14/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_mother_ships_by_id_(self):
        client = APIClient()
        response = client.get(self.url + '1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_mother_ship(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)