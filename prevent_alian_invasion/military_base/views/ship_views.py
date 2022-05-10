from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from military_base.models import MotherShip, Ship, CrewMember
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import permissions
from military_base.serializers import ShipSerializer
# Create your views here.


# get products with search, pagination
@api_view(['GET'])
def getShips(request):
    _ships = Ship.objects.all()
    serializer = ShipSerializer(_ships, many=True)
    return Response({'_ships': serializer.data})

@api_view(['GET'])
def getShipById(request, pk):
    _ships = Ship.objects.get(_id=pk)
    serializer = ShipSerializer(_ships, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def createShip(request):
    data = request.data
    _ms = MotherShip.objects.filter(code = data["code"])
    
    # checking if the mother ship exists
    if len(_ms) < 1:
        message = {"Error": True,  "message": "The mothership does not exist"}
        return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
    # Checking if the mother ship is not full
    if len(_ms) >= 9:
        message = {"Error": True,  "message": "The mothership is already full"}
        return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    # check if data given contain ship and has all necessary data
    ship = data["ship"]
    if "ship" not in data or ship is None or len(ship) < 1:
        message = {"Error": True, "message": "The ship detail has to be provided"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if data provided contains the details for members.
    if  ship["members"] is None or len(ship["members"]) < 1:
        message = {"Error": True, "message": "Atleast 3 members has to be provided"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if members are atleast 3.
    if len(ship["members"]) < 3:
        message = {"Error": True, "message": "Atleast 3 members has to be provided"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the ship already exists
    _s = Ship.objects.filter(code = ship['code'])
    if len(_s) > 0:
        message = {"Error": True, "message": "The ship code already exists."}
        return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    # Check if any crew member given does not exist
    for member in ship["members"]:
        if member is None:
            message = {"Error": True, "message": "Atleast 3 members has to be provided"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        _m = CrewMember.objects.filter(code = member["code"])
        if len(_m) > 0:
            message = {"Error": True, "message": "One of the members already exists."}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    # Creating the Ship object
    _ship = Ship.objects.create(
        mother = _ms[0],
        name = ship['name'],
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
    return Response(data)


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