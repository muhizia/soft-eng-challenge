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
        self.url = '/api/ship/'
        mother = MotherShip.objects.create(id=1, code="x-r")
        Ship.objects.create(mother = mother, id=14, code="x-r-n")
        
    def getJsonFile(self, value):
        path = '{}/ship/ship_json/'.format(self.BASE_DIR) + value + '.json'
        mother_json = open(path)
        mother_json = json.load(mother_json)
        return mother_json
        
    def test_create_ship_ship_success_1(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile( "success"), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_ship_ship_fail_1(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile( "fail_1"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_ship_ship_fail_2(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("fail_2"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_ship_ship_fail_3(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("fail_3"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_ship_ship_fail_4(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("fail_4"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_ship_ship_fail_5(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("fail_5"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_ship_ship_fail_6(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("fail_6"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_ship_ship_fail_7(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("fail_7"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_ship_ship_fail_8(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("fail_8"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_ship_ship_fail_9(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("fail_9"), format='json')
        self.assertEqual(response.status_code, status.HTTP_507_INSUFFICIENT_STORAGE)
        
    def test_create_ship_ship_success_2(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("success_2"), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)