from KYBAPI.models import Bus,Destination,SubDestination,State,Country
from KYBAPI.MESSAGES.Names import Names

from KYBAPI.UTILITY.ResponseBack import ResponseBack
from KYBAPI.MESSAGES.ResponseCode import ResponseCode
from KYBAPI.MESSAGES.ResponseMessages import ResponseMessage

class DestinationController:

    # Get destination data
    def GetDestinationsData(self,Dest_id):
        try:
            #print(f"get destination data {Dest_id}")
            destination = Destination.objects.filter(id = Dest_id).first()

            data = {
                Names.NAME:destination.name,
                Names.ID:destination.id
            }
            return ResponseBack(status=ResponseCode.SUCCESS,
                                data=data,
                                message= ResponseMessage.DESTINATION_DATA_SUCCESS,
                                local=True)
        except Exception as e:
            return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.DESTINATION_DATA_ERROR,
                                local=True)
        

    # Get initial destination
    def GetDestinations(self,dest_str):
        try:
            destinations = Destination.objects.filter(name__icontains=dest_str).order_by('name')

            destination_list = []
            for destination in destinations:
                #print(destination.id)
                destdataresp = self.GetDestinationsData(Dest_id=destination.id)
                #print(f"destdataresp {destdataresp.data}")

                data = {
                    Names.STATUS:destdataresp.status,
                    Names.DATA:destdataresp.data
                }

                destination_list.append(data)
                #print(f"destination_list {destination_list}")
            return ResponseBack(status=ResponseCode.SUCCESS,
                                data=destination_list,
                                message= ResponseMessage.DESTINATION_FOUND_SUCCESS,
                                local=True)
        except Exception as e:
            return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.DESTINATION_FOUND_ERROR,
                                local=True)
    
    #Bilk destiantion creator
    def CreateBulkDestinations(self,data):
        try:
            for item in data:
                state = item.get(Names.STATE)
                upbusid = item.get(Names.ID)
                state_inst= State.objects.filter(name=state).first()
                if state_inst is None:
                    country = Country.objects.all().first()
                    state_inst = State.objects.create(name=state,country=country)
                destination = Destination.objects.create(name=item.get(Names.LOCATION),state=state_inst,up_loc_id=upbusid)
            return ResponseBack(status=ResponseCode.SUCCESS,
                                data={},
                                message= ResponseMessage.DESTINATION_CREATED_SUCCESS,
                                local=True)
        except Exception as e:
            return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.DESTINATION_FOUND_ERROR,
                                local=True)