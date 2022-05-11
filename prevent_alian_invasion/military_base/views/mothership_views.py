import os
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from military_base.models import MotherShip, Ship, CrewMember
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import permissions
from military_base.serializers import MotherShipSerializer, ShipSerializer
from dotenv import load_dotenv
load_dotenv()

# get products with search, pagination
@api_view(['GET'])
def getMotherShips(request):
    mother_ships = MotherShip.objects.all()

    serializer = MotherShipSerializer(mother_ships, many=True)
    return Response({'mother_ships': serializer.data}, status.HTTP_200_OK)

@api_view(['GET'])
def getMotherShipById(request, pk):
    mother_ships =  MotherShip.objects.filter(id=pk).first()
    if mother_ships is None:
        message = {"Error": True, "message": str(os.getenv('MOTHER_SHIP_NOT_FOUND'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    serializer = MotherShipSerializer(mother_ships, many=False)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def createMotherShip(request):
    data = request.data
    _ms = MotherShip.objects.filter(code = data['code'])
    if "ships" not in data:
        message = {"Error": True, "message": str(os.getenv('ENTITY_NOT_PROVIDED'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    # checking the duplicity of the Mother ship
    if len(_ms) > 0:
        message = {"Error": True, "message": str(os.getenv('MOTHER_CODE_EXISTS'))}
        return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    # Check the ship sent are valid
    if data['ships'] is None or len(data['ships']) < 3:
        message = {"Error": True,  "message": str(os.getenv('THREE_SHIPS_FAI'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    # loop through ships to check if they have crew members
    for ship in data['ships']:
        if ship is None or len(ship) < 3:
            message = {"Error": True, "message": str(os.getenv('THREE_SHIPS_FAIL'))}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the ship has enough space
        if len(ship) >= 9:
            message = {"Error": True, "message": str(os.getenv('MOTHER_SHIP_NOT_ENOUGH'))}
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        # checking the duplicity of the Mother ship
        # _c stands for the ship object.
        # 
        _s = Ship.objects.filter(code = ship['code'])
        if len(_s) > 0:
            message = {"Error": True, "message": str(os.getenv('SHIP_EXISTS'))}
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        # loop through given members
        for member in ship["members"]:
            if member is None or len(member) < 3:
                message = {"Error": True, "message": str(os.getenv('THREE_MEMBER_FAIL'))}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            
            if len(member) >= 5:
                message = {"Error": True, "message": str(os.getenv('SHIP_NOT_ENOUGH'))}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            _cm = Ship.objects.filter(code = ship['code'])
            if len(_cm) > 0:
                message = {"Error": True, "message": str(os.getenv('MEMBER_EXISTS'))}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    mother_ships = MotherShip.objects.create(
        name = data['name'],
        code = data['code'],
    )
    for ship in data['ships']:
        _ship = Ship.objects.create(
            mother = mother_ships,
            name = ship['name'],
            code = ship['code'],
        )
        for member in ship["members"]:
            CrewMember.objects.create(
                ship = _ship,
                firstName = member['first_name'],
                lastName = member['last_name'],
                code = member['code'],
                isOfficer = member['is_officer']
            )
    # serializer = MotherShipSerializer(mother_ships, many=False)
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def updateMotherShip(request, pk):
    data = request.data
    mother_ships = MotherShip.objects.get(id=pk)

    mother_ships.name = data ['name']
    mother_ships.code = data ['code']
    mother_ships.save()

    serializer = MotherShipSerializer(mother_ships, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteMotherShip(request, pk):
    mother_ships = MotherShip.objects.get(id=pk)
    mother_ships.delete()
    return Response('MOTHERSHIP deleted')