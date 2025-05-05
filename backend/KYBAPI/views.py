from django.shortcuts import render
from .models import Bus,Destination,SubDestination,Clicks
from KYBAPI.CONTROLLERS.BusController.Buscontroller import BusController
from KYBAPI.CONTROLLERS.DestinationController.Destinationcontroller import DestinationController
from KYBAPI.CONTROLLERS.RouteController.RouteController import RouteController

from KYBAPI.UTILITY.ResponseBack import ResponseBack
from KYBAPI.MESSAGES.ResponseCode import ResponseCode
from KYBAPI.MESSAGES.ResponseMessages import ResponseMessage
from rest_framework.decorators import api_view
from KYBAPI.MESSAGES.Names import Names
from django.template.loader import render_to_string 
# Create your views here.

def Home(request):
    start_loc = Destination.objects.filter(id = 103).first()
    end_loc = Destination.objects.filter(id = 101).first()
    busresp = RouteController().GetIndirectBusRoute(initial_dest=start_loc,Final_dest=end_loc)
    return render(request,'routecard.html',{"routes":busresp.data})
# get bus from initial
@api_view(['GET'])
def BusInitial(request,initial_loc):
    try:
        #print(f"initial_loc {initial_loc} type {type(initial_loc)}")
        location = Destination.objects.filter(id = initial_loc).first()
        #print(f"location {location}")

        busresp = BusController().GetBusInitial(from_destination_id = location.id)
        #print(f"busresp {busresp.data}")
        # rendered_html = render_to_string('buscard.html', {"buses": busresp.data})

        return ResponseBack(status=busresp.status,
                            # data=rendered_html,#html render serverside
                            data=busresp.data,
                            message= busresp.message)
    except Exception as e:
        return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.BUS_INITIAL_ERROR)

# bus from final
@api_view(['GET'])
def Busfinal(request,final_loc):
    try:
        #print(f"initial_loc {initial_loc} type {type(initial_loc)}")
        location = Destination.objects.filter(id = final_loc).first()
        #print(f"location {location}")

        busresp = BusController().GetBusFinal( final_destination_id= location.id)
        #print(f"busresp {busresp.data}")
        # rendered_html = render_to_string('buscard.html', {"buses": busresp.data})

        return ResponseBack(status=busresp.status,
                            # data=rendered_html,#html serverside rendering
                            data=busresp.data,
                            message= busresp.message)
    except Exception as e:
        return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.BUS_FINAL_ERROR)
# get bus
@api_view(['GET'])
def GetBus(request):
    try:
        initial_loc = request.GET.get(Names.INITIAL_LOC)
        final_loc = request.GET.get(Names.FINAL_LOC)
        print(f"initial_loc {initial_loc} type {type(initial_loc)}")
        print(f"final_loc {final_loc} type {type(final_loc)}")

        start_loc = Destination.objects.filter(id=int(initial_loc)).first()
        end_loc = Destination.objects.filter(id=int(final_loc)).first()

        busresp = BusController().GetBus(from_loc_id=start_loc.id, final_loc_id=end_loc.id)

        # Render the buscard.html template with dynamic data
        # rendered_html = render_to_string('buscard.html', {"buses": busresp.data})

        # Prepare the response object with the rendered HTML
        return ResponseBack(
            status= busresp.status,
            message= busresp.message,
            data= busresp.data
        )
    except Exception as e:
        return ResponseBack(
            status=ResponseCode.ERROR,
            data=str(e),
            message=ResponseMessage.BUS_NOT_FOUND
        )

@api_view(['GET'])
def GetAllBus(request):
    try:
        busresp = BusController().GetAllBus()
        return ResponseBack(status=busresp.status,
                                data=busresp.data,
                                message= busresp.message)
    except Exception as e:
        return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.BUS_NOT_FOUND)
#get route
@api_view(['GET'])
def GetRoute(request):
    try:
        initial_loc = request.GET.get(Names.INITIAL_LOC)
        final_loc = request.GET.get(Names.FINAL_LOC)
        print(f"initial_loc {initial_loc} type {type(initial_loc)}")
        print(f"final_loc {final_loc} type {type(final_loc)}")

        start_loc = Destination.objects.filter(id = int(initial_loc)).first()
        end_loc = Destination.objects.filter(id = int(final_loc)).first()

        busresp = RouteController().GetIndirectBusRoute(initial_dest=start_loc,Final_dest=end_loc)
        # print(busresp.data)
        # print(busresp)
        # render_html=render_to_string('routecard.html',{"routes":busresp.data})
        return ResponseBack(status=busresp.status,
                                data=busresp.data,
                                message= busresp.message)
    except Exception as e:
        return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.BUS_NOT_FOUND)
# get bus extra data
@api_view(['GET'])
def GetBusExtra(request):
    try:
        bus_id = request.GET.get(Names.ID)
        busresp = BusController().GetBusExtraData(bus_id=bus_id)
        return ResponseBack(status=busresp.status,
                                data=busresp.data,
                                message= busresp.message)
    except Exception as e:
        return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.BUS_NOT_FOUND)

# get destination
@api_view(['GET'])
def GetDesinations(request,dest_str):
    try:
        destresp = DestinationController().GetDestinations(dest_str)
        
        return ResponseBack(status=destresp.status,
                                data=destresp.data,
                                message= destresp.message)
    except Exception as e:
        return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.BUS_NOT_FOUND)


# add click
@api_view(['POST'])
def AddClick(request):
    try:
        bus_id = int(request.POST.get(Names.ID))
        bus = Bus.objects.filter(id=bus_id)
        
        from_loc = bus.startdestination

        final_loc = bus.finaldestination

        Clicks.objects.create(startdestination = from_loc,finaldestination = final_loc,fare=bus.fare,distance= bus.distance)

        return ResponseBack(status=ResponseCode.ERROR,
                                data={},
                                message= ResponseMessage.CLICK_ADDED_SUCCESS)
    except Exception as e:
        return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.CLICK_ADDED_ERROR)


@api_view(['POST'])
def CreateBulkDestination(request):
    try:
        destresp = DestinationController().CreateBulkDestinations(request.data)
        
        return ResponseBack(status=destresp.status,
                                data=destresp.data,
                                message= destresp.message)
    except Exception as e:
        return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.BUS_CREATED_ERROR)

@api_view(['POST'])
def CreateBulkBus(request):
    try:
        busresp = BusController().CreateBulkBus(request.data)
        
        return ResponseBack(status=busresp.status,
                                data=busresp.data,
                                message= busresp.message)
    except Exception as e:
        return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.BUS_CREATED_ERROR)