from KYBAPI.models import Bus,Destination,SubDestination
from KYBAPI.MESSAGES.Names import Names
import datetime
import requests
from KYBAPI.UTILITY.ResponseBack import ResponseBack
from KYBAPI.MESSAGES.ResponseCode import ResponseCode
from KYBAPI.MESSAGES.ResponseMessages import ResponseMessage
class BusController:

    # get bus data
    """
    This function will get the data of the bus
    """
    def GetBusData(self,bus_id):
        try:
            #print(f"get bus data {bus_id}")
            bus = Bus.objects.filter(id = bus_id).first()

            #print(f"bus {bus}")
            startdestination ={
                Names.ID:bus.startdestination.id,
                Names.NAME:bus.startdestination.name
            }
            finaldestination={
                Names.ID:bus.finaldestination.id,
                Names.NAME:bus.finaldestination.name
            }
            bus_data = {
                    Names.ID: bus.id,
                    Names.START_TIME : bus.start_time,
                    Names.FINAL_TIME : bus.reaching_time,
                    Names.INITIAL_DEST : startdestination,
                    Names.FINAL_DEST : finaldestination,
                    Names.CATEGORY : bus.category,
                    Names.DISTANCE : bus.distance,
                    Names.ONLINE: bus.online_avilable
                }
            #print(f"bus_data {bus_data}")
            return ResponseBack(status=ResponseCode.SUCCESS,
                                data=bus_data,
                                message= ResponseMessage.BUS_DATA_FOUND_SUCCESS,
                                local=True)
        except Exception as e:
            return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.BUS_DATA_FOUND_ERROR,
                                local=True)
    
    def GetAllBus(self):
        try:
            buses = Bus.objects.all()
            bus_list = []
            for bus in buses:
                data = {
                   Names.INITIAL_DEST:bus.startdestination.name,
                   Names.FINAL_DEST:bus.finaldestination.name
                }
                bus_list.append(data)
            return ResponseBack(status=ResponseCode.SUCCESS,
                                data=bus_list,
                                message= ResponseMessage.BUS_FOUND,
                                local=True)
        except Exception as e:
            return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.BUS_NOT_FOUND,
                                local=True)
    # get bus extra detail
    def GetBusExtraData(self,bus_id):
        try:
            #print(f"get bus data {bus_id}")
            bus = Bus.objects.filter(id = bus_id).first()

            #print(f"bus {bus}")
            startdestination ={
                Names.ID:bus.startdestination.id,
                Names.NAME:bus.startdestination.name
            }
            finaldestination={
                Names.ID:bus.finaldestination.id,
                Names.NAME:bus.finaldestination.name
            }
            bus_data = {
                    Names.ID: bus.id,
                    Names.START_TIME : bus.start_time,
                    Names.FINAL_TIME : bus.reaching_time,
                    Names.INITIAL_DEST : startdestination,
                    Names.FINAL_DEST : finaldestination,
                    Names.ONLINE_AVILABLE: bus.online_avilable,
                    Names.BOOKING_LINK: bus.booking_link,
                    Names.MAP_LINK: bus.start_map_link,
                    Names.FARE : bus.category,
                    Names.DISTANCE : bus.distance,
                }
            #print(f"bus_data {bus_data}")
            return ResponseBack(status=ResponseCode.SUCCESS,
                                data=bus_data,
                                message= ResponseMessage.BUS_DATA_FOUND_SUCCESS,
                                local=True)
        except Exception as e:
            return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.BUS_DATA_FOUND_ERROR,
                                local=True)

    
    
    #get bus
    """
    This function gets the buses from 
    initial to final location
    and store there data in bus list to be send as a response
    """
    def GetBus(self,from_loc_id,final_loc_id):
        try:
            from_destination = Destination.objects.filter(id = from_loc_id).first()
            final_destination = Destination.objects.filter(id = final_loc_id).first()

            buses = Bus.objects.filter(startdestination = from_destination,
                                    finaldestination = final_destination,
                                    confirmed=True)
            # print(buses)
            print(f" length {len(buses)}")
            if len(buses) == 0:
                uprouteresp = self.UPRouteData(from_destination,final_destination)
                # print(f"uprouteresp {uprouteresp}")
                buses = Bus.objects.filter(startdestination = from_destination,
                                    finaldestination = final_destination,
                                    confirmed=True)
            print(f"buses\n {buses}")
            bus_list = []
            for bus in buses:
                busdataresp = self.GetBusData(bus_id = bus.id)
                data = {
                    Names.STATUS:busdataresp.status,
                    Names.DATA:busdataresp.data
                }
                bus_list.append(data)
            
            return ResponseBack(status=ResponseCode.SUCCESS,
                                # data=buses, #for serverside html
                                data=bus_list,
                                message= ResponseMessage.BUS_FOUND,
                                local=True)
        
        except Exception as e:
            return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.BUS_NOT_FOUND,
                                local=True)
        
    # get bus with initial
    """
    This fuction gets the buses from intial location
    and store there data in bus list to be send as a response
    """
    def GetBusInitial(self,from_destination_id):
        try:

            destination = Destination.objects.filter(id = from_destination_id).first()

            # print(f"destination {destination}")

            buses = destination.startdestinations.all()
            # print(f"buses {buses}")

            bus_list = []
            for bus in buses:
                busdataresp = self.GetBusData(bus_id = bus.id)
                data = {
                    Names.STATUS:busdataresp.status,
                    Names.DATA:busdataresp.data
                }
                bus_list.append(data)
            print(f"bus_list {bus_list}")
            return ResponseBack(status=ResponseCode.SUCCESS,
                                # data=buses, #for serverside html
                                data=bus_list,
                                message= ResponseMessage.BUS_FOUND,
                                local=True)
        except Exception as e:
            return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.BUS_NOT_FOUND,
                                local=True)

    # get bus with final
    """
    This fuction gets the buses from final location
    and store there data in bus list to be send as a response
    """
    def GetBusFinal(self,final_destination_id):
        try:
            destination = Destination.objects.filter(id = final_destination_id).first()

            buses = destination.finaldestinations.filter(confirmed=True)

            bus_list = []
            for bus in buses:
                busdataresp = self.GetBusData(bus_id = bus.id)
                data = {
                    Names.STATUS:busdataresp.status,
                    Names.DATA:busdataresp.data
                }
                bus_list.append(data)
            print(f"bus_list {bus_list}")

            return ResponseBack(status=ResponseCode.SUCCESS,
                                # data=buses, #for serverside html
                                data=bus_list,
                                message= ResponseMessage.BUS_FOUND,
                                local=True)
        except Exception as e:
            return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.BUS_NOT_FOUND, 
                                local=True)
        
    #bus bulk creatoin
    def CreateBulkBus(self,data):
        try:
            for item in data:
                # print(f"item {item}")
                start_dest = item.get(Names.FROM_LOC)
                final_dest = item.get(Names.FINAL_LOC)
                category = item.get(Names.CATEGORY)
                online = item.get(Names.ONLINE)
                start_time = item.get(Names.START_TIME)
                booking_link = item.get(Names.BOOKING_LINK)
                final_time = item.get(Names.FINAL_TIME)
                start_destination = Destination.objects.filter(name=start_dest).first()
                final_destination = Destination.objects.filter(name=final_dest).first()
                
                # print(f'{start_destination.id,final_destination.id,category,online,time,booking_link}\n')
                if online:
                    bus = Bus.objects.create(startdestination=start_destination,finaldestination=final_destination,online_avilable=True,category=category,booking_link = booking_link,confirmed=True,start_time = start_time,final_time = final_time)
                else:
                    bus = Bus.objects.create(startdestination=start_destination,finaldestination=final_destination,confirmed=True,online_avilable=False,category=category,start_time = start_time,final_time = final_time)
            return ResponseBack(status=ResponseCode.SUCCESS,
                                data={},
                                message= ResponseMessage.BUS_CREATED_SUCCESS,
                                local=True)
        except Exception as e:
            return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.BUS_CREATED_ERROR,
                                local=True)
    # up route
    def UPRouteData(self,loc1, loc2):
        url = "https://onlineupsrtc.co.in:8081/upsrtc/api/booking/v2/bus/seats"

        payload_template = {
            "outboundTripDate": None,
            "qrType": 1,
            "scheduleId": None,
            "products": [
                {"productCode": "1", "passengerCount": 1},
                {"productCode": "2", "passengerCount": 0},
                {"productCode": "3", "passengerCount": 0},
                {"productCode": "7", "passengerCount": 0}
            ],
            "sourceStation": "",
            "destinationStation": "",
            "inboundTripDate": get_current_timestamp(),
            "busType": "0"
        }

        # Set dynamic station IDs based on location
        payload = payload_template.copy()
        payload["sourceStation"] = str(loc1.up_loc_id)  
        payload["destinationStation"] = str(loc2.up_loc_id)

        try:
            response = requests.post(url, json=payload, verify=False)

            if response.status_code == 200:
                api_data = response.json()
                # print(f"req data = {api_data}")

                new_routes = []
                # print(f"new_routes = {api_data.get('tickets')}")
                
                for ticket in api_data.get("tickets", []):
                        ticket_data = {
                            Names.FROM_LOC: ticket.get("startStationName"),
                            Names.FINAL_LOC: ticket.get("endStationName"),
                            Names.CATEGORY: ticket.get("busType"),
                            Names.FINAL_TIME: ticket.get("endTime"),
                            Names.START_TIME: ticket.get("stationArrivalTime"),
                            Names.ONLINE: True,
                            Names.BOOKING_LINK: 'https://www.onlineupsrtc.co.in/#/home'
                        }
                        new_routes.append(ticket_data)
                createbusresp = self.CreateBulkBus(new_routes)
                print(f"createbusresp = {createbusresp}")
                if createbusresp.status == ResponseCode.ERROR:
                    return ResponseBack(status=ResponseCode.SUCCESS,
                                data=createbusresp.data,
                                message= ResponseMessage.UP_ROUTE_FOUND,
                                local=True)

                return ResponseBack(status=ResponseCode.SUCCESS,
                                data=createbusresp.data,
                                message= ResponseMessage.UP_ROUTE_FOUND_CREATED,
                                local=True)

            else:
                return ResponseBack(status=ResponseCode.ERROR,
                                data=createbusresp.data,
                                message= ResponseMessage.UP_ROUTE_ERROR,
                                local=True)

        except requests.exceptions.RequestException as e:
            return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message= ResponseMessage.UP_ROUTE_ERROR,
                                local=True)


# timestamp
def get_current_timestamp():
    """Generate a current timestamp in the format YYYYMMDDHHMMSS."""
    now = datetime.datetime.now() + datetime.timedelta(days=1)
    return now.strftime("%Y%m%d%H%M%S")
