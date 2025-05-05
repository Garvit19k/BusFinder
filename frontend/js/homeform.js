$(document).ready(function () {
    // Handle the selection of items in the dropdown
    $(".dropdown-item").on("click", function () {
        const selectedValue = $(this).text();  // Get the text of the selected item
        const targetInput = $(this).closest('.input-group').find('input');  // Find the related input field
        targetInput.val(selectedValue);  // Set the value of the input field
    });

    // Example of form submission handling
    $("form").on("submit", function (event) {
        event.preventDefault();
    
        const fromDestination = $("#from").data('value');
        const toDestination = $("#to").data('value');

        console.log(fromDestination, toDestination);
        // Check if the form values are valid and different
        window.location.href = `routes.html?from=${fromDestination}&to=${toDestination}`;
    });
});

