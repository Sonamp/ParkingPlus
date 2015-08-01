from django.db import models

# Create your models here.
#model for floor plan
class FloorPlan(models.Model):
    floorNo = models.SmallIntegerField(unique = True)
    totalParking = models.IntegerField()
    availableParking = models.IntegerField(null = True)
    
    def __str__(self):
        return str(self.floorNo)

#model for car entry exit information
class CarEntryExit(models.Model):
    carNo = models.CharField(max_length= 100)
    floorNo = models.SmallIntegerField()
    timeEntered = models.DateTimeField()
    timeExit = models.DateTimeField(null = True)
    feePaid = models.FloatField(null = True)
    
    def __unicode__(self):
        return self.carNo