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
        
        
    
    def getJsonFile(self, value):
        path = '/Users/muhizi/Documents/fulgel/soft-eng-challenge/mother_json/mother' + value + '.json'
        mother_fail_4 = open(path)
        mother_fail_4 = json.load(mother_fail_4)
        return mother_fail_4
        
        
    def test_get_mother_ships(self):
        client = APIClient()
        response = client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_mother_ships_by_id(self):
        client = APIClient()
        response = client.get(self.url + '14/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_mother_ships_by_wrong_id(self):
        client = APIClient()
        response = client.get(self.url + '1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_mother_ship_success_1(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile( "_success"), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_mother_ship_fail_1(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile( "_fail_1"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_mother_ship_fail_2(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("_fail_2"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_mother_ship_fail_3(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("_fail_3"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_mother_ship_fail_4(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("_fail_4"), format='json')
        self.assertEqual(response.status_code, status.HTTP_507_INSUFFICIENT_STORAGE)
        
    def test_create_mother_ship_fail_5(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("_fail_5"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_mother_ship_fail_6(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("_fail_6"), format='json')
        self.assertEqual(response.status_code, status.HTTP_507_INSUFFICIENT_STORAGE)
        
    # def test_create_mother_ship_success_2(self):
    #     client = APIClient()
    #     response = client.post(self.url + 'create/', self.getJsonFile("_fail_7"), format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)