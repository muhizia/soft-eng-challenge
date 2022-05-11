import os
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from military_base.models import CrewMember, Ship
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import permissions
from military_base.serializers import CrewMemberSerializer
from dotenv import load_dotenv
load_dotenv()

# get products with search, pagination
@api_view(['GET'])
def getCrewMembers(request):
    _crews = CrewMember.objects.all()
    serializer = CrewMemberSerializer(_crews, many=True)
    return Response({'_crews': serializer.data})

@api_view(['GET'])
def getCrewMemberById(request, pk):
    _crews = CrewMember.objects.get(id=pk)
    serializer = CrewMemberSerializer(_crews, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def createCrewMember(request):
    data = request.data
    _s = Ship.objects.filter(code = data["code"])
    
    # checking if the mother ship exists
    if len(_s) < 1:
        message = {"Error": True,  "message": str(os.getenv('SHIP_NOT_EXISTS'))}
        return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    # check if data given contain ship and has all necessary data
    crew_member = data["members"]
    if "members" not in data or crew_member is None or len(crew_member) < 1:
        message = {"Error": True, "message": str(os.getenv('MEMBER_DETAIL_FAILS'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    # Checking if the mother ship is not full
    _c = CrewMember.objects.filter(ship = _s[0])
    if len(_c) + len(crew_member) > 5:
        message = {"Error": True,  "message": str(os.getenv('SHIP_NOT_ENOUGH'))}
        return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    # Check if any crew member given does not exist
    for member in crew_member:
        if member is None:
            message = {"Error": True, "message": str(os.getenv('THREE_MEMBER_FAIL'))}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    for member in crew_member:
        # Creating a crew member of the ship
        CrewMember.objects.create(
            ship = _s[0],
            firstName = member['first_name'],
            lastName = member['last_name'],
            code = member['code'],
            isOfficer = member['is_officer']
        )
    return Response(data)


@api_view(['PUT'])
def updateCrewMember(request, pk):
    data = request.data
    _crews = CrewMember.objects.get(id=pk)

    _crews.firstName = data ['first_name']
    _crews.lastName = data ['last_name']
    _crews.code = data ['code']
    _crews.isOfficer = data ['is_officer']
    _crews.save()

    serializer = CrewMemberSerializer(_crews, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def moveCrewMember(request, pk):
    data = request.data
    if "from_ship" not in data or "to_ship" not in data:
        message = {"Error": True, "message": str(os.getenv('FROM_FAIL'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    if data["from_ship"] is None or data["to_ship"] is None:
        message = {"Error": True, "message": str(os.getenv('FROM_FAIL'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    to_ship = Ship.objects.filter(code=data["to_ship"]).first()
    from_ship = Ship.objects.filter(code=data["from_ship"]).first()
    if to_ship is None:
        message = {"Error": True, "message": str(os.getenv('TO_NOT_EXISTS'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    if from_ship is None:
        message = {"Error": True, "message": str(os.getenv('FROM_NOT_EXISTS'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    crews = CrewMember.objects.filter(ship = to_ship)
    if len(crews) >= 4:
        message = {"Error": True, "message": str(os.getenv('SHIP_NOT_ENOUGH'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    _crew = CrewMember.objects.filter(ship=from_ship, id=pk).first()
    if _crew is None:
        message = {"Error": True, "message": str(os.getenv('NAME_NOT_EXISTS'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
   
    _crew.ship = to_ship
    _crew.save()
    serializer = CrewMemberSerializer(_crew, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteCrewMember(request, pk):
    ships = CrewMember.objects.get(id=pk)
    ships.delete()
    return Response('CREW MEMBER deleted')