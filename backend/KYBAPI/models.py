from django.db import models

# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey('Country', on_delete=models.CASCADE,related_name="state")

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
# destination (name ,state ,country)
class Destination(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    up_loc_id = models.CharField(max_length=100,null=True,blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE,related_name="destination_state",null=True,blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,related_name="destination_country",null=True,blank=True)
    google_link=models.CharField(max_length=2500,null=True,blank=True)
    def __str__(self):
        return self.name
class Bus_service(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
# bus (start time ,reaching time ,startdestination ,final destination,sub destination, fare, confirmed, distance)
class Bus(models.Model):
    bus_service = models.ForeignKey(Bus_service, on_delete=models.CASCADE,related_name="bus_service",null=True,blank=True)
    start_time = models.CharField(max_length=10,null=True,blank=True)
    final_time = models.CharField(max_length=10,null=True,blank=True)
    reaching_time = models.CharField(max_length=10,null=True,blank=True)
    startdestination = models.ForeignKey(Destination, on_delete=models.CASCADE,related_name="startdestinations",null=True,blank=True)
    finaldestination = models.ForeignKey(Destination, on_delete=models.CASCADE,related_name="finaldestinations",null=True,blank=True)
    category = models.CharField(max_length=20,null=True,blank=True)
    start_map_link=models.CharField(max_length=2500,null=True,blank=True)
    distance = models.CharField(max_length=20,null=True,blank=True)
    booking_link = models.CharField(max_length=2500,null=True,blank=True)
    company = models.CharField(max_length=100,null=True,blank=True)
    online_avilable = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.startdestination.name} to {self.finaldestination.name}"

# subdestination (bus, name, distance, time,S.NO)
class SubDestination(models.Model):
    bus = models.ForeignKey(Bus,related_name="Sub_Destination", on_delete=models.CASCADE)
    destinationName = models.ForeignKey(Destination,on_delete=models.CASCADE)
    distance = models.IntegerField()
    time = models.CharField( max_length=50)
    SNO = models.IntegerField()
    
    def __str__(self):
        return f"{self.bus} buses sub-destination no {self.SNO}"
    
    
# clicks (start destination , final destination, fare, date, distance)
class Clicks(models.Model):
    startdestination = models.ForeignKey(Destination,on_delete=models.CASCADE,related_name="start_destination_click")
    finaldestination = models.ForeignKey(Destination,on_delete=models.CASCADE,related_name="final_destination_click")
    fare = models.CharField(max_length=10)
    date = models.DateField(auto_now=False, auto_now_add=False)
    distance = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.start_destination.name} to {self.final_destination.name}"