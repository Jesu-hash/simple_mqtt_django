  // load current chart package
  google.charts.load("current", {
    packages: ["corechart", "line"]
});

// set callback function when api loaded
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

    // create data object with default value
    let data = google.visualization.arrayToDataTable([
        ["Year", "CPU Usage"],
        [0, 0]
    ]);

    // create options object with titles, colors, etc.
    let options = {
        title: "CPU Usage",
        hAxis: {
            title: "Time"
        },
        vAxis: {
            title: "Usage"
        }
    };

    // draw chart on load
    let chart = new google.visualization.LineChart(
        document.getElementById("chart_div")
    );
    chart.draw(data, options);

    // interval for adding new data every 250ms
    let index = 0;
    setInterval(function() {

        // instead of this random, you can make an ajax call for the current cpu usage or what ever data you want to display
        let random = Math.random() * 30 + 20;

        data.addRow([index, random]);
        chart.draw(data, options);

        index++;
    }, 250);

}