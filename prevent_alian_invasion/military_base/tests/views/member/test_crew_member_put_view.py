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
        self.url = '/api/crewmember/update/'
        mother = MotherShip.objects.create(id=1, code="x-r")
        ship = Ship.objects.create(mother = mother, id=14, code="01-INV")
        CrewMember.objects.create(ship = ship, id=14, code="x-r-nc", isOfficer = False, firstName="Aristide", lastName="Muhizi")
    
    def getJsonFile(self, value):
        path = '{}/member/crew_json/crew'.format(self.BASE_DIR) + value + '.json'
        _json = open(path)
        _json = json.load(_json)
        return _json
    
    def test_put_crew_member_by_wrong_id(self):
        client = APIClient()
        response = client.put(self.url + '1/',self.getJsonFile('_update_fail_1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_put_crew_member_by_id_1(self):
        client = APIClient()
        response = client.put(self.url + '14/',self.getJsonFile('_update_fail_2'), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_put_crew_member_by_id_2(self):
        client = APIClient()
        response = client.put(self.url + '14/',self.getJsonFile('_update_success'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)