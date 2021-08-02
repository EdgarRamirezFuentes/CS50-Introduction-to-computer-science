document.addEventListener("DOMContentLoaded", (e) => {
    const calendar_container = document.getElementById("calendar_container");
    let calendar_events;
    const calendar = new FullCalendar.Calendar(calendar_container, {
        timeZone: 'local',
        locale: 'es',
        //initialView: "timeGridDay",
    });

    fetch(`/get-tasks`, {
        // Adding method type
        method: "GET",
    })
    // Converting to JSON
    .then(response => response.json())
    // Displaying information to its container
    .then((data) => {
        if (data) {
            data.forEach((event) => {
                calendar.addEvent(event);
            });
        }
    })
    .catch(console.warn);
    
    calendar.render();
});
