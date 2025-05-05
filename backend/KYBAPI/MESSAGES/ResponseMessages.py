class ResponseMessage:

    DEFAULT_ERROR = "Something went wrong"
    DEFAULT_SUCESS = "Completed successfully"
    DEFAULT_NOT_FOUND = "Not found"

    # bus messages
    BUS_NOT_FOUND= "Bus not found"
    BUS_FOUND = "Bus found"

    BUS_INITIAL_ERROR = "Bus with initial location not found"
    BUS_FINAL_ERROR = "Bus with final location not found"

    BUS_DATA_FOUND_SUCCESS = "Bus data found"
    BUS_DATA_FOUND_ERROR =  "Bus data not found"

    BUS_CREATED_SUCCESS = "Bus created successfully"
    BUS_CREATED_ERROR = "Bus not created"

    # clicks
    CLICK_ADDED_SUCCESS = "Click added sucessfully"
    CLICK_ADDED_ERROR= "Click not added"
    CLICK_ADDED_SUCCESS = "Click added successfully"
    CLICK_ADDED_ERROR = "Click added successfully"

    # Destination
    DESTINATION_FOUND_SUCCESS="Destination found"
    DESTINATION_FOUND_ERROR = "Destination not found"
    DESTINATION_DATA_SUCCESS = "Get detination data Sucessful"
    DESTINATION_DATA_ERROR = "Unable to get detination data"
    DESTINATION_CREATED_SUCCESS = "Destinations created sucessfully"

    # route
    ROUTE_FOUND_SUCCESS = "Route found"
    ROUTE_FOUND_ERROR = "Route not found"

    #UP specific
    UP_ROUTE_ERROR = "UP route not found"
    UP_ROUTE_FOUND_CREATED = "UP route found and created"
    UP_ROUTE_FOUND = "UP route found not created"




