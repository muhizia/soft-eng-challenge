from django.db import models
from django.utils import timezone

# Create your models here.


class MotherShip(models.Model):
    code       = models.CharField(max_length=200, null=False, blank=False, unique=True)
    name       = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
        
class Ship(models.Model):
    mother     = models.ForeignKey(MotherShip, on_delete=models.CASCADE ,null=False)
    code       = models.CharField(max_length=200, null=False, blank=False, unique=True)
    name       = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
        
class CrewMember(models.Model):
    ship       = models.ForeignKey(Ship, on_delete=models.CASCADE, null=False)
    firstName  = models.CharField(max_length=200, null=False, blank=False, unique=True)
    lastName   = models.CharField(max_length=200, null=False, blank=False)
    code       = models.CharField(max_length=200, null=False, blank=False)
    isOfficer  = models.BooleanField(default=False)
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code