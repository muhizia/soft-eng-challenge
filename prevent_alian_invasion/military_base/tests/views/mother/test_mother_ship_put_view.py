import json
from pathlib import Path
from django.test import TestCase, Client
from django.urls import reverse, resolve
from military_base.models import MotherShip, Ship, CrewMember
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class TestViews(TestCase):
    
    def setUp(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.url = '/api/mothership/update/'
        MotherShip.objects.create(id=14, code="x-r")
    
    def getJsonFile(self, value):
        path = '{}/mother/mother_json/mother'.format(self.BASE_DIR) + value + '.json'
        _json = open(path)
        _json = json.load(_json)
        return _json
    def test_put_mother_ships_by_wrong_id(self):
        client = APIClient()
        response = client.put(self.url + '1/',self.getJsonFile('_update_fail_1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_put_mother_ships_by_id_1(self):
        client = APIClient()
        response = client.put(self.url + '14/',self.getJsonFile('_update_fail_1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_put_mother_ships_by_id_2(self):
        client = APIClient()
        response = client.put(self.url + '14/',self.getJsonFile('_update_fail_2'), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_put_mother_ships_by_id_3(self):
        client = APIClient()
        response = client.put(self.url + '14/',self.getJsonFile('_update_fail_3'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)