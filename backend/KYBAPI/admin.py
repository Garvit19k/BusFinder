from django.contrib import admin
from .models import Bus,Destination,SubDestination,Clicks,State,Country,Bus_service
# Register your models here.

admin.site.register(Bus)
admin.site.register(Destination)
admin.site.register(SubDestination)
admin.site.register(Clicks)
admin.site.register(State)
admin.site.register(Country)
admin.site.register(Bus_service)