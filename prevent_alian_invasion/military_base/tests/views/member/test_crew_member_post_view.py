import json
from pathlib import Path
from django.test import TestCase, Client
from military_base.models import MotherShip, Ship, CrewMember
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class TestViews(TestCase):
    
    def setUp(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.url = '/api/crewmember/'
        mother = MotherShip.objects.create(id=1, code="x-r")
        ship = Ship.objects.create(mother = mother, id=14, code="01-INV")
        CrewMember.objects.create(ship = ship, id=14, code="x-r-nc", isOfficer = False, firstName="Aristide", lastName="Muhizi")
        
    def getJsonFile(self, value):
        path =  '{}/member/crew_json/crew_'.format(self.BASE_DIR) + value + '.json'
        mother_json = open(path)
        mother_json = json.load(mother_json)
        return mother_json
        
    def test_create_crew_member_success_1(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("success"), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_crew_member_fail_1(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile( "fail_1"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_crew_member_fail_2(self):
        client = APIClient()
        # testing null
        response = client.post(self.url + 'create/', self.getJsonFile("fail_2"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # testing empty
        response = client.post(self.url + 'create/', self.getJsonFile("fail_4"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_crew_member_fail_3(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("fail_3"), format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        
    def test_create_crew_member_fail_4(self):
        client = APIClient()
        response = client.post(self.url + 'create/', self.getJsonFile("fail_5"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)