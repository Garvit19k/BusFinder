// Function to get query parameters from the URL
function getQueryParams() {
    const urlParams = new URLSearchParams(window.location.search);
    return {
        from: urlParams.get('from'),
        to: urlParams.get('to')
    };
}
// function to make api request to get bus data
function fetchBusData(initial_loc, final_loc) {
    const baseurl = `http://127.0.0.1:8000/api/`
    var dataurl = `get_bus/`
    // console.log(initial_loc, "---", final_loc)
    if (final_loc === 'undefined' || final_loc === '') {
        // console.log("final_loc is undefined")
        dataurl = `bus_initial/${initial_loc}/`
    }
    if (initial_loc === 'undefined' || initial_loc === '') {
        // console.log("final_loc is undefined")
        dataurl = `bus_final/${final_loc}/`
    }

    $.ajax({
        url: baseurl + dataurl,
        method: "GET",
        data: {
            "start_location": initial_loc,
            "final_location": final_loc
        },
        success: function (data) {
            console.log("success")
            console.log(data)
            $("#bus-container").empty();
            // $("#bus-container").append(data.data);
            populateBus(data.data);
            detailclick()
        },
        error: function (xhr, status, error) {
            console.log("Error fetching bus data:", error);
        }
    });
    if (dataurl === `get_bus/`) {
        $.ajax({
            url: baseurl + 'get_route/',
            method: "GET",
            data: {
                "start_location": initial_loc,
                "final_location": final_loc
            },
            success: function (data) {
                console.log(data)
                const busData = data.data;
                const $busContainer = $("#bus-container2");
                $busContainer.empty();
                // $busContainer.append(busData);
                populaterroute(busData);
                detailclick()
            },
            error: function (xhr, status, error) {
                console.log("Error fetching bus data:", error);
            }
        });
    }

}

function dropdownsearch() {
    $('#from').on('input', function () {
        const searchTerm = $(this).val().toLowerCase();  // Get the input value and convert to lowercase

        // Iterate over all dropdown items and show/hide based on the search term
        $('#dropdownItems .dropdown-item').each(function () {
            const itemText = $(this).text().toLowerCase();  // Get the text of the current item and convert to lowercase

            if (itemText.includes(searchTerm)) {
                $(this).show();  // Show the item if it matches the search term
            } else {
                $(this).hide();  // Hide the item if it doesn't match the search term
            }
        });
    });
}
// check if parma inurl and call ajax
function handleQueryParams() {
    const urlParams = new URLSearchParams(window.location.search);
    const initial_loc = urlParams.get("from");
    const final_loc = urlParams.get("to");
    // console.log(initial_loc, final_loc);

    if (initial_loc && final_loc) {
        fetchBusData(initial_loc, final_loc);  // Call the function to fetch bus data
    }
}
function inputfilter() {
    $(document).ready(function () {

        $('.form-control').on('input', function () {
            var $inputValue = $(this).val().toLowerCase();
            const $itemobj = $(this).attr("id");

            $('.dropdown-menu li').each(function () {
                var itemText = $(this).text().toLowerCase();
                const $item = $(`.${$itemobj}-dropdown-menu`);
                $item.show();
                // console.log($inputValue=="",$inputValue==" ")
                if (itemText.includes($inputValue)) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
                if ($inputValue == "") {
                    $item.hide();
                }
                $item.on("click", function () {
                    $item.hide();
                });
            });
        });
    });

}
$(document).ready(function () {

    handleQueryParams();
    dropdownsearch();

});

// <div class="card border-primary mb-3 w-100">
//     <div class="card-body d-flex flex-column align-items-md-center justify-content-between">
//         <div class="route d-flex align-items-center w-100">
//             <span class="from fw-bold me-2">${bus["start_destination"].name}</span>
//             <div class="flex-grow-1 border-top border-secondary"></div>
//             <span class="to fw-bold ms-2">${bus["final_destination"].name}</span>
//         </div>
//         <div class="details mt-3 mt-md-0 d-flex flex-wrap justify-content-between align-items-center">
//             <div class="text-center me-3">
//                 <span class="d-block">category</span>
//                 <span>${bus["category"]}</span>
//             </div>
//             <div class="text-center me-3">
//                 <span class="d-block">Distance</span>
//                 <span>${bus["distance"]} KM</span>
//             </div>
//             <div class="text-center me-3">
//                 <span class="d-block">Departure</span>
//                 <span>${bus["start_time"]}</span>
//             </div>
//             <div class="text-center me-3">
//                 <span class="d-block">Online</span>
//                 <span>${bus["online"]}</span>
//             </div>
//             <button class="btn btn-primary detail-btn" data-id="${bus['id']}">detail</button>
//         </div>
//     </div>
// </div>

// removed 
// // populate bus data in page
function populateBus(busData) {
    // console.log(busData)
    $busContainer = $("#bus-container");
    // console.log(busData)
    // console.log(busData.length)
    if (busData.length === 0) {
        // Add "No bus found" message
        $busContainer.append(`<h2 class="text-center">No bus found</h2>`);
    } else {
        // console.log(busData)
        // for (buses in busData) {
        //     bus = busData[buses].data
        //     console.log(bus)
        //     onlinestatus = "Offline"
        //     if (bus["online"] === true) {
        //         onlinestatus = "Online"
        //     }
        //     // Create a new card with the bus details
        //     const busCard = `
        //     <div class="col-lg-4 col-md-6 col-sm-12 mb-4">
        //     <div class="bus-card">
        //         <div class="bus-header">
        //             <div>
        //                 <span class="bus-category">${bus["category"]}</span>
        //                 <div class="status online">${onlinestatus}</div>
        //             </div>
        //             <div class="icon-circle">
        //                 🚍
        //             </div>
        //         </div>

        //         <div class="progress mt-2">
        //             <div class="progress-bar" style="width: 80%;"></div>
        //         </div>

        //         <div class="bus-info mt-3">
        //             <div>
        //                 <span>Start</span>
        //                 <br>
        //                 <small>${bus["start_destination"].name}</small>
        //             </div>
        //             <div>
        //                 <span>Final</span>
        //                 <br>
        //                 <small>${bus["final_destination"].name}</small>
        //             </div>
        //         </div>

        //         <div class="bus-info mt-2">
        //             <div>
        //                 <span>${bus["start_time"]}</span>
        //             </div>
        //             <div>
        //                 <span>${bus["start_time"]}</span>
        //             </div>
        //         </div>

        //         <div class="text-end mt-3">
        //             <button class="detail-btn" data-id="${bus['id']}">Details</button>
        //         </div>
        //     </div>
        // </div>
        // `;

        //     $busContainer.append(busCard);

        // }
        busData.forEach(buses => {
            // console.log(buses.data)
            bus = buses.data
            onlinestatus = "Offline"
            if (bus["online"] === true) {
                onlinestatus = "Online"
            }
            // Create a new card with the bus details
            const busCard = `
            <div class="col-lg-4 col-md-6 col-sm-12 mb-4">
            <div class="bus-card">
                <div class="bus-header">
                    <div>
                        <span class="bus-category">${bus["category"]}</span>
                        <div class="status online">${onlinestatus}</div>
                    </div>
                    <div class="icon-circle">
                        🚍
                    </div>
                </div>

                <div class="progress mt-2">
                    <div class="progress-bar" style="width: 80%;"></div>
                </div>

                <div class="bus-info mt-3">
                    <div>
                        <span>Start</span>
                        <br>
                        <small>${bus["start_destination"].name}</small>
                    </div>
                    <div>
                        <span>Final</span>
                        <br>
                        <small>${bus["final_destination"].name}</small>
                    </div>
                </div>

                <div class="bus-info mt-2">
                    <div>
                        <span>${bus["start_time"]}</span>
                    </div>
                    <div>
                        <span>${bus["start_time"]}</span>
                    </div>
                </div>

                <div class="text-end mt-3">
                    <button class="detail-btn" data-id="${bus['id']}">Details</button>
                </div>
            </div>
        </div>
        `;

            $busContainer.append(busCard);  // Make sure you have a div with id "bus-container"
        });
    }
    detailclick()
}

// Populate roude 
function populaterroute(busData) {
    const $busContainer = $("#bus-container2");
    $busContainer.empty();
    // console.log(busData)
    // console.log(busData.length)
    if (busData.length === 0) {
        // Add "No bus found" message
        $busContainer.append(`<h2 class="text-center">No bus found</h2>`);
    } else {
        // console.log(busData)
        busData.forEach(buses => {
            // console.log(buses.data)
            first_bus = buses.first_bus
            last_bus = buses.second_bus
            // Create a new card with the bus details
            const busCard = `
            <div class="col-lg-4 col-md-6 col-sm-12 mb-4">
            <div class="bus-card">
                <div class="bus-header">
                    <div>
                        <span class="bus-category">ASC Bus</span>
                        <div class="status online">${bus["online"]}</div>
                    </div>
                    <div class="icon-circle">
                        🚍
                    </div>
                </div>

                <div class="progress mt-2">
                    <div class="progress-bar" style="width: 80%;"></div>
                </div>

                <div class="bus-info mt-3">
                    <div>
                        <span>Initial</span>
                        <br>
                        <small>${first_bus["start_destination"].name}</small>
                    </div>
                    <div>
                    <span>Change</span>
                        <br>
                        <small>${first_bus["final_destination"].name}</small>
                    </div>
                    <div>
                        <span>Final</span>
                        <br>
                        <small>${last_bus["final_destination"].name}</small>
                    </div>
                </div>

                <div class="bus-info mt-2">
                    <div>
                        <span>Start Time:${first_bus["start_time"]}</span>
                    </div>
                    <div>
                        <span>Arrival:${first_bus["start_time"]}</span>
                    </div>
                </div>
                

                <div class="text-end mt-3">
                    <button class="detail-btn" data-id="${first_bus["id"]}">Details</button>
                </div>
            </div>
        </div>
        `;
            $busContainer.append(busCard);
        });
    }
    detailclick()
}