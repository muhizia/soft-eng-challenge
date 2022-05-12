import os
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from military_base.models import CrewMember, Ship
from rest_framework.decorators import api_view
from military_base.utils import util
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
    _crews = CrewMember.objects.filter(id=pk).first()
    if _crews is None:
        message = {"Error": True, "message": str(os.getenv('CREW_NOT_FOUND'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    serializer = CrewMemberSerializer(_crews, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def createCrewMember(request):
    data = request.data
    # check if the code for the ship is given
    if "code" not in data or data['code'] is None:
        message = {"Error": True, "message": str(os.getenv('SHIP_NOT_EXISTS'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    # checking if the mother ship exists
    _s = Ship.objects.filter(code = data["code"])
    if len(_s) < 1:
        message = {"Error": True,  "message": str(os.getenv('SHIP_NOT_EXISTS'))}
        return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    # check if data given contain ship and has all necessary data
    crew_member = data["members"]
    if "members" not in data or crew_member is None or len(crew_member) < 1:
        message = {"Error": True, "message": str(os.getenv('MEMBER_DETAIL_FAILS'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    # Checking if the mother ship is not full
    _c = CrewMember.objects.filter(ship = _s.first())
    if len(_c) >= 5:
        message = {"Error": True,  "message": str(os.getenv('SHIP_NOT_ENOUGH'))}
        return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    # Checking if all required are given
    if "first_name" not in crew_member or "last_name" not in crew_member or crew_member["first_name"] is None or crew_member["last_name"] is None:
        message = {"Error": True, "message": str(os.getenv('MEMBER_DETAIL_FAILS'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    util.insert_into_crew_member(crew_member, _s.first())
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def updateCrewMember(request, pk):
    data = request.data
    _crews = CrewMember.objects.filter(id=pk)
    if len(_crews) < 1:
        message = {"Error": True, "message": str(os.getenv('CREW_NOT_FOUND'))}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    
    if "first_name" not in data or "last_name" not in data or data["first_name"] is None or data["last_name"] is None:
        message = {"Error": True, "message": str(os.getenv('MEMBER_DETAIL_FAILS'))}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    _crews = _crews.first()
    _crews.firstName = data ['first_name']
    _crews.lastName = data ['last_name']
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
    if len(crews) >= 5:
        message = {"Error": True, "message": str(os.getenv('SHIP_NOT_ENOUGH'))}
        return Response(message, status=status.HTTP_507_INSUFFICIENT_STORAGE)
    
    _crew = CrewMember.objects.filter(ship=from_ship, id=pk).first()
    if _crew is None:
        message = {"Error": True, "message": str(os.getenv('NAME_NOT_EXISTS'))}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
   
    _crew.ship = to_ship
    _crew.save()
    serializer = CrewMemberSerializer(_crew, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteCrewMember(request, pk):
    # check if the selected mother ship exists
    crew = CrewMember.objects.filter(id=pk)
    if len(crew) < 1:
        message = {"Error": True, "message": str(os.getenv('CREW_NOT_FOUND'))}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    # delete crew member
    crew = CrewMember.objects.get(id=pk)
    crew.delete()
    return Response('CREW MEMBER deleted')