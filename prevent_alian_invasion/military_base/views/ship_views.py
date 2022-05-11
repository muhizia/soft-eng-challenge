import os
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from military_base.models import MotherShip, Ship, CrewMember
from military_base.utils import util
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import permissions
from military_base.serializers import ShipSerializer
from dotenv import load_dotenv
load_dotenv()

# get products with search, pagination
@api_view(['GET'])
def getShips(request):
    _ships = Ship.objects.all()
    serializer = ShipSerializer(_ships, many=True)
    return Response({'_ships': serializer.data}, status.HTTP_200_OK)

@api_view(['GET'])
def getShipById(request, pk):
    _ships = Ship.objects.filter(id=pk).first()
    if _ships is None:
        message = {"Error": True, "message": str(os.getenv('SHIP_NOT_EXISTS'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    serializer = ShipSerializer(_ships, many=False)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def createShip(request):
    data = request.data
    
    # check if data given contain ship 
    if "ship" not in data:
        message = {"Error": True, "message": str(os.getenv('MOTHER_CODE_NOT_PROVIDED'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    # check if data given contain ship and has all necessary data
    ship = data["ship"]
    if ship is None or ship is None or len(ship) < 1:
        message = {"Error": True, "message": str(os.getenv('SHIP_DETAIL_FAILS'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    _ms = MotherShip.objects.filter(code = data["code"])
    
    # checking if the mother ship exists
    if len(_ms) < 1:
        message = {"Error": True,  "message": str(os.getenv('MOTHER_SHIP_NOT_EXISTS'))}
        return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    # Checking if the mother ship is not full
    if len(_ms) >= 9:
        message = {"Error": True,  "message": str(os.getenv('MOTHER_SHIP_NOT_ENOUGH'))}
        return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    # Check if data provided contains the details for members.
    if  "members" not in ship or ship["members"] is None or len(ship["members"]) < 1:
        message = {"Error": True, "message": str(os.getenv('THREE_MEMBER_FAIL'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    if  "code" not in ship or ship["code"] is None:
        message = {"Error": True, "message": str(os.getenv('CODE_NOT_PROVIDED'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if members are atleast 3.
    if len(ship["members"]) < 3:
        message = {"Error": True, "message":  str(os.getenv('THREE_MEMBER_FAIL'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if members are atleast 3.
    if len(ship["members"]) > 5:
        message = {"Error": True, "message":  str(os.getenv('SHIP_NOT_ENOUGH'))}
        return Response(message, status=status.HTTP_507_INSUFFICIENT_STORAGE)
    
    # Check if the ship already exists
    _s = Ship.objects.filter(code = ship['code'])
    if len(_s) > 0:
        message = {"Error": True, "message":  str(os.getenv('SHIP_CODE_EXISTS'))}
        return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    # Check if any crew member given does not exist
    util.check_member(ship)
    
    name = '' if "name" not in ship else ship['name']
    # Creating the Ship object
    _ship = Ship.objects.create(
        mother = _ms[0],
        name = name,
        code = ship['code'],
    )
    for member in ship["members"]:
        # Creating a crew member of the ship
        CrewMember.objects.create(
            ship = _ship,
            firstName = member['first_name'],
            lastName = member['last_name'],
            code = member['code'],
            isOfficer = member['is_officer']
        )
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def updateShip(request, pk):
    data = request.data
    _ships = Ship.objects.get(_id=pk)

    _ships.name = data ['name']
    _ships.code = data ['code']
    _ships.save()

    serializer = ShipSerializer(_ships, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteShip(request, pk):
    ships = Ship.objects.get(id=pk)
    ships.delete()
    return Response('SHIP deleted')