import os
from rest_framework import status
from rest_framework.response import Response
from military_base.models import MotherShip, Ship, CrewMember
from dotenv import load_dotenv
load_dotenv()

def check_member(ship):
    # loop through given members
    for member in ship["members"]:
        if member is None or len(ship["members"]) < 3:
            message = {"Error": True, "message": str(os.getenv('THREE_MEMBER_FAIL'))}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
        _m = CrewMember.objects.filter(code = member["code"])
        if len(_m) > 0:
            message = {"Error": True, "message": str(os.getenv('MEMBER_EXISTS'))}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)