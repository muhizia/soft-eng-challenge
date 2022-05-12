import json
from django.test import TestCase, Client
from django.urls import reverse, resolve
from military_base.models import MotherShip, Ship, CrewMember
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class TestViews(TestCase):
    
    def setUp(self):
        self.url = '/api/crewmember/delete/'
        mother = MotherShip.objects.create(id=1, code="x-r")
        ship = Ship.objects.create(mother = mother, id=14, code="01-INV")
        CrewMember.objects.create(ship = ship, id=14, code="x-r-nc", isOfficer = False, firstName="Aristide", lastName="Muhizi")
    
    def test_put_ships_by_wrong_id(self):
        client = APIClient()
        response = client.delete(self.url + '1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_put_ships_by_id_1(self):
        client = APIClient()
        response = client.delete(self.url + '14/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)