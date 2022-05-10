from django.shortcuts import render
from rest_framework.response import Response
from military_base.models import MotherShip
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import permissions
from military_base.serializers import MotherShipSerializer, ShipSerializer
# Create your views here.


# get products with search, pagination
@api_view(['GET'])
def getMotherShips(request):
    mother_ships = MotherShip.objects.all()

    serializer = MotherShipSerializer(mother_ships, many=True)
    return Response({'mother_ships': serializer.data})

@api_view(['GET'])
def getMotherShipById(request, pk):
    mother_ships = MotherShip.objects.get(_id=pk)
    serializer = MotherShipSerializer(mother_ships, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def createMotherShip(request):
    data = request.data
    mother_ships = MotherShip.objects.create(
        name = data ['name'],
        code = data ['code'],
    )
    serializer = MotherShipSerializer(mother_ships, many=False)
    return Response(serializer.data)




@api_view(['PUT'])
def updateMotherShip(request, pk):
    data = request.data
    mother_ships = MotherShip.objects.get(_id=pk)

    mother_ships.name = data ['name']
    mother_ships.code = data ['code']
    mother_ships.save()

    serializer = MotherShipSerializer(mother_ships, many=False)
    return Response(serializer.data)




@api_view(['DELETE'])
def deleteMotherShip(request, pk):
    mother_ships = MotherShip.objects.get(_id=pk)
    mother_ships.delete()
    return Response('Product deleted')