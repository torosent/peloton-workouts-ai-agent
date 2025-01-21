document.addEventListener("DOMContentLoaded", function () {

    const calendarEl = document.getElementById("calendar");

    // Map the weekly plan into FullCalendar events
    let events = [];
    if (weeklyPlan != undefined) {
        events = [];
        Object.keys(weeklyPlan).forEach((weekKey) => {
            const days = weeklyPlan[weekKey];
            days.forEach((dayObj) => {
                dayObj.activities.forEach((activity) => {
                    if (activity.title === "Rest Day") {
                        events.push({
                            date: dayObj.day,
                            title: "Rest Day",
                            description: "Take a break and relax!"
                        });
                    } else {
                        events.push({
                            date: dayObj.day,
                            title: `${activity.category}: ${activity.title} with ${activity.instructor} - ${activity.description}`,
                            url: activity.url,
                            description: `
                                <strong>Duration:</strong> ${activity.duration} mins<br>
                                <strong>Instructor:</strong> ${activity.instructor}<br>
                                <strong>Intensity:</strong> ${activity.intensity}<br>
                                <strong>Info:</strong> ${activity.extra_info}<br>                  `
                        });
                    }
                });
            });
        });
    }


    

    // Initialize FullCalendar
    const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'listWeek',
            headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: "timeGridWeek,timeGridDay",
        },
        events: events,
        eventDidMount: function (info) {
            const tooltip = new bootstrap.Tooltip(info.el, {
                title: info.event.extendedProps.description,
                html: true,
            });
        }
    });

    calendar.render();
});
