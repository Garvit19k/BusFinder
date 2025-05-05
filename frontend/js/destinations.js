function searchevent() {
    $('.dropdown-item').each(function () {

        $(this).on('click', function () {
            // Get the text content of the selected option
            let start_dest = $('#from')[0].dataset.value;
            let final_dest = $('#to')[0].dataset.value;

            console.log(`start_dest ${typeof (start_dest)} ${$("#from").val()}\nfinal_dest ${final_dest} ${$("#to").val()}`);
            if (final_dest === undefined || final_dest === '0') {
                fetchBusData(start_dest, 'undefined');
            } else if (start_dest === undefined || start_dest === '0') {
                fetchBusData('undefined', final_dest);
            }
            else {
                fetchBusData(start_dest, final_dest);
            }
        });
    });
}
function populateDropdown(data) {
    $(".dropdown-menu").each(function () {
        const $dropdownMenu = $(this);
        const datavalue = $dropdownMenu.attr("date-value");

        $dropdownMenu.empty();

        $dropdownMenu.append('<li><a class="dropdown-item" data-value="0" style="color:gray;">Select destination</a></li>');

        data.forEach((item) => {
            let item_data = item.data;
            $dropdownMenu.append(
                `<li><a class="dropdown-item ${datavalue}-dropdown-item" data-value="${item_data.id}">${item_data.name}</a></li>`
            );
        });
    });

    inputfilter()
    $(".dropdown-menu").find("a").on("click", function (event) {
        const selectedValue = $(this).data("value");
        const selectedText = $(this).text();

        $(this).closest(".input-group").find("input").val(selectedText);
        $(this).closest(".input-group").find("input").attr("data-value", selectedValue);

    });
    searchevent()
    dropdownsearch()

}

$(document).ready(function () {
    $('.form-control').on('input', function () {
        var $inputValue = $(this).val().toLowerCase();
        if ($inputValue.length == 3) {
            console.log("calling api")
            const apiUrl = `http://127.0.0.1:8000/api/get_destination/${$inputValue}/`;
            $.ajax({
                url: apiUrl,
                method: "GET",
                dataType: "json",
                success: function (data) {
                    if (data.status === 200 && data.data) {

                        const destinations = data.data;
                        populateDropdown(destinations);
                    } else {
                        console.error("Error fetching destinations:", data.message);
                    }
                },
                error: function (xhr, status, error) {
                    console.error("Error fetching destinations:", error);
                }
            });
        }
    })




});
