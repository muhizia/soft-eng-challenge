from military_base.models import MotherShip, Ship, CrewMember
from rest_framework import serializers


class MotherShipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MotherShip
        fields = ['id', 'code', 'name']


class ShipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ship
        fields = ['id', 'code', 'name']