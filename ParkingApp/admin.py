from django.contrib import admin
from ParkingApp.models import FloorPlan, CarEntryExit
# Register your models here.
class FloorAdmin(admin.ModelAdmin):
    list_display = ('floorNo', 'totalParking', 'availableParking')
    list_filter = ['floorNo']
    
class CarEntryExitAdmin(admin.ModelAdmin):
    list_display = ('carNo', 'floorNo', 'timeEntered', 'timeExit', 'feePaid')
    list_filter = ['timeEntered', 'timeExit', 'floorNo']
    
    
admin.site.register(FloorPlan, FloorAdmin)
admin.site.register(CarEntryExit, CarEntryExitAdmin)