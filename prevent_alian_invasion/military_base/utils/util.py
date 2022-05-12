import os
from rest_framework import status
from rest_framework.response import Response
from military_base.models import MotherShip, Ship, CrewMember
from dotenv import load_dotenv
load_dotenv()


def check_members(ship):
    # loop through given members
    for member in ship["members"]:
        if member is None or len(ship["members"]) < 3:
            message = {"Error": True, "message": str(os.getenv('THREE_MEMBER_FAIL'))}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
        _m = CrewMember.objects.filter(code = member["code"])
        if len(_m) > 0:
            message = {"Error": True, "message": str(os.getenv('MEMBER_EXISTS'))}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
def insert_into_ship(data, mother_ships):
    for ship in data['ships']:
        ship_parent = Ship.objects.create(
            mother = mother_ships,
            name = ship['name'],
            code = ship['code'],
        )
        loop_through_member(ship, ship_parent)
        
def loop_through_member(ship, ship_parent):
    for member in ship["members"]:
        insert_into_crew_member(member, ship_parent)

def insert_into_crew_member(member, ship_parent):
    isOfficer = False if "is_officer" not in member else member['is_officer']
    CrewMember.objects.create(
        ship = ship_parent,
        firstName = member['first_name'],
        lastName = member['last_name'],
        code = member['code'],
        isOfficer = isOfficer
    )

# def check_member(crew_member):
#     if "first_name" not in crew_member or "last_name" not in crew_member or "code" not in crew_member or crew_member["first_name"] is None or crew_member["last_name"] is None or crew_member["code"] is None:
#         message = {"Error": True, "message": str(os.getenv('MEMBER_DETAIL_FAILS'))}
#         return Response(message, status=status.HTTP_400_BAD_REQUEST)
#     print('--->', crew_member)