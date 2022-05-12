import json
from django.test import TestCase, Client
from military_base.models import MotherShip, Ship, CrewMember
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class TestViews(TestCase):
    
    def setUp(self):
        self.url = '/api/crewmember/'
        mother = MotherShip.objects.create(id=1, code="x-r")
        ship = Ship.objects.create(mother = mother, id=14, code="x-r-n")
        CrewMember.objects.create(ship = ship, id=14, code="x-r-nc", isOfficer = False, firstName="Aristide", lastName="Muhizi")
        
        
    def test_get_crew_members(self):
        client = APIClient()
        response = client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_crew_member_by_id(self):
        client = APIClient()
        response = client.get(self.url + '14/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_crew_member_by_wrong_id(self):
        client = APIClient()
        response = client.get(self.url + '1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)