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
        self.url = '/api/crewmember/move/'
        mother = MotherShip.objects.create(id=1, code="x-r")
        ship1 = Ship.objects.create(mother = mother, id=14, code="01-INV")
        ship2 = Ship.objects.create(mother = mother, id=15, code="02-INV")
        CrewMember.objects.create(ship = ship1, id=14, code="x-r-nc", isOfficer = False, firstName="Aristide", lastName="Muhizi")
        
    def insert_into_crew(self):
        mother = MotherShip.objects.create(id=3, code="x-r-1")
        ship = Ship.objects.create(mother = mother, id=6, code="04-INV")
        CrewMember.objects.create(ship = ship, id=16, code="x-r-nc-1", isOfficer = False, firstName="Aristide", lastName="Muhizi")
        CrewMember.objects.create(ship = ship, id=17, code="x-r-nc-2", isOfficer = False, firstName="Aristide", lastName="Muhizi")
        CrewMember.objects.create(ship = ship, id=18, code="x-r-nc-3", isOfficer = False, firstName="Aristide", lastName="Muhizi")
        CrewMember.objects.create(ship = ship, id=19, code="x-r-nc-4", isOfficer = False, firstName="Aristide", lastName="Muhizi")
        CrewMember.objects.create(ship = ship, id=20, code="x-r-nc-5", isOfficer = False, firstName="Aristide", lastName="Muhizi")
        
    def getJsonFile(self, value):
        path = '{}/member/crew_json/crew'.format(self.BASE_DIR) + value + '.json'
        _json = open(path)
        _json = json.load(_json)
        return _json
    
    def test_move_crew_member_by_wrong_id(self):
        client = APIClient()
        response = client.put(self.url + '1/', self.getJsonFile('_move_success'), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_put_crew_member_by_id_1(self):
        client = APIClient()
        response = client.put(self.url + '14/',self.getJsonFile('_move_fail_1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_put_crew_member_by_id_2(self):
        client = APIClient()
        response = client.put(self.url + '14/',self.getJsonFile('_move_fail_2'), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_put_crew_member_by_id_3(self):
        client = APIClient()
        response = client.put(self.url + '14/',self.getJsonFile('_move_fail_3'), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_put_crew_member_by_id_4(self):
        client = APIClient()
        self.insert_into_crew()
        response = client.put(self.url + '14/',self.getJsonFile('_move_fail_4'), format='json')
        self.assertEqual(response.status_code, status.HTTP_507_INSUFFICIENT_STORAGE)
        
    def test_put_crew_member_by_id_5(self):
        client = APIClient()
        response = client.put(self.url + '14/',self.getJsonFile('_move_success'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)