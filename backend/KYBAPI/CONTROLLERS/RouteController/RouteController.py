from KYBAPI.models import Bus,Destination,SubDestination
from KYBAPI.MESSAGES.Names import Names
from KYBAPI.CONTROLLERS.BusController.Buscontroller import BusController
from KYBAPI.CONTROLLERS.DestinationController.Destinationcontroller import DestinationController

from KYBAPI.UTILITY.ResponseBack import ResponseBack
from KYBAPI.MESSAGES.ResponseCode import ResponseCode
from KYBAPI.MESSAGES.ResponseMessages import ResponseMessage
from datetime import datetime,timedelta
class RouteController():
    BusController =BusController()
    DestinationController = DestinationController()

    def convert_to_datetime(self,time_str):
        try:
            # print(f"time_str {time_str}")
            return datetime.strptime(time_str, "%I:%M %p")
        except ValueError:
            return None

    def GetIndirectBusRoute(self, initial_dest, Final_dest):
        try:
            BusFromInitial = initial_dest.startdestinations.filter(confirmed=True)
            BusFromFinal = Final_dest.finaldestinations.filter(confirmed=True)

            # print(f"BusFromInitial {BusFromInitial}\n")
            # print(f"BusFromFinal {BusFromFinal}\n")

            route_data = []

            for Initial_Bus in BusFromInitial:
                Final_Of_initial = Initial_Bus.finaldestination
                # print(f"Final_Of_initial {Final_Of_initial}\n")
                for Final_Bus in BusFromFinal:
                    Initial_Of_final = Final_Bus.startdestination
                    # print(f"Initial_Of_final {Initial_Of_final}\n")
                    if Initial_Of_final == Final_Of_initial:
                        # Get bus data
                        Initial_Bus_Data = self.BusController.GetBusData(bus_id=Initial_Bus.id)
                        Final_Bus_data = self.BusController.GetBusData(bus_id=Final_Bus.id)
                        # sub_dest_data = self.DestinationController.GetDestinationsData(Dest_id=Initial_Of_final.id)
                        
                        # initial_start_time = self.convert_to_datetime(Initial_Bus_Data.data[Names.FINAL_TIME])
                        initial_start_time = self.convert_to_datetime(Initial_Bus.start_time)
                        final_start_time = self.convert_to_datetime(Final_Bus.start_time)
                        
                        
                        if initial_start_time and final_start_time:
                            time_diff = initial_start_time - final_start_time

                            if time_diff < timedelta(hours=1) and time_diff > timedelta(seconds=0):
                                
                                data = {
                                    'first_bus': Initial_Bus_Data,
                                    'second_bus': Final_Bus_data,
                                    Names.CHANGE_LOC: Initial_Of_final
                                }
                                route_data.append(data)

            return ResponseBack(status=ResponseCode.ERROR,
                                    data=route_data,
                                    message=ResponseMessage.ROUTE_FOUND_SUCCESS,
                                    local=True)
        except Exception as e:
            print(e)
            return ResponseBack(status=ResponseCode.ERROR,
                                data=str(e),
                                message=ResponseMessage.ROUTE_FOUND_ERROR,
                                local=True)
    # get indirect bus route
    # def GetIndirectBusRoute(self,initial_dest,Final_dest):
    #     try:
    #         BusFromInitial = initial_dest.startdestinations.filter(confirmed=True)
    #         BusFromFinal = Final_dest.finaldestinations.filter(confirmed=True)
    #         print(f"BusFromInitial {BusFromInitial}\n")
    #         print(f"BusFromFinal {BusFromFinal}\n")


    #         route_data=[]

    #         for Initial_Bus in BusFromInitial:
    #             Final_Of_initial = Initial_Bus.finaldestination
    #             for Final_Bus in BusFromFinal:

    #                 Initial_Of_final = Final_Bus.startdestination
    #                 print(f"{Initial_Of_final == Final_Of_initial}\n")
    #                 if Initial_Of_final == Final_Of_initial:
    #                     Initial_Bus_Data = self.BusController.GetBusData(bus_id=Initial_Bus.id)
    #                     Final_Bus_data = self.BusController.GetBusData(bus_id=Final_Bus.id)
    #                     sub_dest_data = self.DestinationController.GetDestinationsData(Dest_id = Initial_Of_final.id)
                        
    #                     data ={
    #                         'first_bus': Initial_Bus_Data.data,
    #                         'second_bus': Final_Bus_data.data,
    #                         Names.CHANGE_LOC: sub_dest_data.data
    #                     }

    #                     route_data.append(data)

    #         return ResponseBack(status=ResponseCode.ERROR,
    #                             data=route_data,
    #                             message= ResponseMessage.ROUTE_FOUND_SUCCESS,
    #                             local=True)
    #     except Exception as e:
    #         return ResponseBack(status=ResponseCode.ERROR,
    #                             data=str(e),
    #                             message= ResponseMessage.ROUTE_FOUND_ERROR,
    #                             local=True)
        
