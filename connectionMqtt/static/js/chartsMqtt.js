  // load current chart package
  google.charts.load("current", {
    packages: ["corechart", "line"]
});

// set callback function when api loaded
google.charts.setOnLoadCallback(drawChart);

// for percentage data
var dashboard, data, chart, options;

var i = 0;

var idSelectedRow = 0

function drawChart() {

    //Create our data table.
    data = new google.visualization.DataTable();
    data.addColumn('number', 'Time');
    data.addColumn('number', 'sensor');

    let idSelected = idSelectedRow.toString();
    let sensorId= 'Data sensor' + ' ' + idSelected;
  
    // create options object with titles, colors, etc.
    options = {
        title: sensorId,
        hAxis: {
            title: "Time"
        },
        vAxis: {
            title: "Data read in real time"
        }
    };

    // draw chart on load
    chart = new google.visualization.LineChart(
        document.getElementById("chart_div")
    );
    chart.draw(data, options);

}

/* update the chart1 - data */
function updateChart(reading) {
    i = (i + 1);

    data.addRow([i, reading]);

    chart.draw(data, options);
}

function addRow(tableID ,id, temp, timestamp) {

    var table = document.getElementById(tableID);

    var rowCount = table.rows.length;
    var row = table.insertRow(rowCount);

    var cell1 = row.insertCell(0);
    cell1.innerHTML = rowCount + 1;

    var cell2 = row.insertCell(1);
    cell2.innerHTML = id;

    var cell3 = row.insertCell(2);
    cell3.innerHTML = temp;

    var cell4 = row.insertCell(3);
    cell4.innerHTML = timestamp;

    //Update rows with event onclick
    select_row();
}

function select_row() {
    var table = document.getElementById('table');
    var cells = table.getElementsByTagName('td');
 
    for (var i = 0; i < cells.length; i++) {
        // Take each cell
        var cell = cells[i];
        // do something on onclick event for cell
        cell.onclick = function () {
            // Get the row id where the cell exists
            var rowId = this.parentNode.rowIndex;

            var rowsNotSelected = table.getElementsByTagName('tr');
            for (var row = 0; row < rowsNotSelected.length; row++) {
                rowsNotSelected[row].style.backgroundColor = "";
                rowsNotSelected[row].style.color = "white";
                rowsNotSelected[row].classList.remove('table-light');
            }
            var rowSelected = table.getElementsByTagName('tr')[rowId];
            //rowSelected.style.backgroundColor = "yellow";
            rowSelected.style.color = "black";
            rowSelected.className += "table-light";
   
            //Column Id
            msg = 'The ID is equal to: ' + rowSelected.cells[1].innerHTML;

            //Save id of row selected
            idSelectedRow = rowSelected.cells[1].innerHTML;
            //Reflesh the draw
            drawChart();

            console.log(msg)
            //msg += '\nThe cell value is: ' + this.innerHTML;
            //alert(msg);
        }
    }

} //end of function

window.onload = select_row;