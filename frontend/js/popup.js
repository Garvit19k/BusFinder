function detailclick() {
  // Add event listeners to all detail buttons
  $(".detail-btn").on("click", function() {
    console.log("detail button clicked");
    const busId = $(this).data("id");
    $.ajax({
      url: "http://127.0.0.1:8000/api/bus_extra_detail/",
      method: "GET",
      data: {
          "id": busId
      },
      success: function(data) {
        // console.log(data.data)
        popuppopulator(data.data)
      },
      error: function(xhr, status, error) {
          console.error("Error fetching bus data:", error);
      }
  });
    
  });
  // cole pop up eventsdaade
  closepopupevents()
}
function popuppopulator(data){
  console.log(data)
  let popupContent = `
      <div class="popup-overlay">
        <div class="popup-content">
          <span class="close-btn">&times;</span>
          <h4>Route Details</h4>`;

    // Add "From" and "To" locations
    if (data.start_destination) {
        popupContent += `<p><strong>From:</strong> ${data.start_destination.name}</p>`;
    }

    if (data.final_destination) {
        popupContent += `<p><strong>To:</strong> ${data.final_destination.name}</p>`;
    }

    // Add "Distance" if available
    if (data.distance) {
        popupContent += `<p><strong>Distance:</strong> ${data.distance}</p>`;
    }

    // Add "Fare" if available
    if (data.fare) {
        popupContent += `<p><strong>category:</strong> ${data.fare}</p>`;
    }

    // Add "Departure Time" if available
    if (data.start_time) {
        popupContent += `<p><strong>Departure Time:</strong> ${data.start_time}</p>`;
    }

    // Add "Arrival Time" if available
    if (data.reaching_time) {
        popupContent += `<p><strong>Arrival Time:</strong> ${data.reaching_time}</p>`;
    }

    // Add Google Map link if available
    if (data.google_map_link) {
        popupContent += `<a href="${data.google_map_link}" target="_blank" class="btn btn-outline-primary map-link">View on Google Maps</a>`;
    }

    // Add Booking Link if available
    if (data.booking_link) {
        popupContent += `<a href="${data.booking_link}" target="_blank" class="btn btn-outline-secondary mt-2 booking-link">Book Now</a>`;
    }

    popupContent += `</div></div>`;  // Close the popup content and overlay div

    // Inject the popup content into the container
    const popupContainer = $("#popup-container");
    popupContainer.html(popupContent);

    // Show the popup
    $(".popup-overlay").fadeIn();
  
}
function closepopupevents(){
  // Close popup function
  $(document).on("click", ".popup-overlay", function() {
    closePopup();
  });
  $(document).on("click", ".close-btn", function() {
    closePopup();
  });
  // Stop propagation to prevent closing when clicking inside the popup content
  $(document).on("click", ".popup-content", function(event) {
    event.stopPropagation();
  });
}
// Close the popup
function closePopup() {
  $(".popup-overlay").fadeOut(function() {
    $(this).remove();
  });
}
const baseurlsarrray = []