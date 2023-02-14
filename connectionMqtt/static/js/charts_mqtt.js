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
var changedSelectedRow = false
var indexDataReceived = 0

function drawChart() {

    //Create our data table.
    data = new google.visualization.DataTable();
    // data.addColumn('number', 'Time');
    // data.addColumn('number', 'sensor');

    let idSelected = idSelectedRow.toString();
    let sensorId= 'Data sensor' + ' ' + idSelected;
  
    var options = {
        hAxis: {
         title: sensorId,
        },
        vAxis: {
          title: 'Data read in real time'
        },
        series: {
          1: {curveType: 'function'}
        }
      };

    // draw chart on load
    chart = new google.visualization.LineChart(
        document.getElementById("chart_div")
    );
    //chart.draw(data, options);

}

function configColumnsChart(keysToDraw) {

    data.addColumn('number', 'X');
    
    for (key in keysToDraw) {
        console.log("configColumnsChart KEY: ",keysToDraw[key]);
        data.addColumn('number', keysToDraw[key]);
    }
//  console.log("data0", data["bf"][0]["label"])
//  console.log("data1", data["bf"][1]["label"])
//  console.log("data1", data["bf"])
//  console.log("data3", data.getColumnIndex("humedity"))
//  console.log("data3", data.getColumnIndex("X"))
 
}
/* update the chart1 - data */
function updateChart(arrayToDraw) {
    //i = (i + 1);

    //console.log(arrayToDraw);
        
    data.addRow(arrayToDraw);

    chart.draw(data, options);
}

function addRow(tableID ,id) {
    var table = document.getElementById(tableID);
    //console.log("document.getElementById(tableID).tHead.innerHTML", document.getElementById(tableID).tHead.innerHTML)
    var element= document.getElementById(tableID).tHead;
    if (element == null){   
    // Create an empty <thead> element and add it to the table:
        var header = table.createTHead();

        // Create an empty <tr> element and add it to the first position of <thead>:
        var rowThead = header.insertRow(0);    
    
        // Insert a new cell (<td>) at the first position of the "new" <tr> element:
        var cell1 = rowThead.insertCell(0);
        var cell2 = rowThead.insertCell(1);
        var cell3 = rowThead.insertCell(2);
        var cell4 = rowThead.insertCell(3);
    
        // Add some bold text in the new cell:
        cell1.innerHTML = "<b>#</b>";
        cell2.innerHTML = "<b>Id</b>";
        cell3.innerHTML = "<b>Data</b>";
        cell4.innerHTML = "<b>Timestamp</b>";

    }
    var rowCount = table.rows.length;
    var row = table.insertRow(rowCount);
    
    row.onmousedown = function(){ RowClick(this,false); }

    var cell1 = row.insertCell(0);
    cell1.innerHTML = rowCount;

    var cell2 = row.insertCell(1);
    cell2.innerHTML = id;

    var cell3 = row.insertCell(2);
    //cell3.innerHTML = temp;

    var cell4 = row.insertCell(3);
    //cell4.innerHTML = timestamp;



 
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
            changedSelectedRow = true;
            indexDataReceived = 0;
            //Reflesh the draw
            drawChart();

            console.log(msg);
            //msg += '\nThe cell value is: ' + this.innerHTML;
            //alert(msg);
        }
    }

} //end of function

//window.onload = select_row;
    var arraIdsSelects = []
    var lastSelectedRow;
    //var trs = document.getElementById('table').tBodies[0].getElementsByTagName('tr');

        // disable text selection
        document.onselectstart = function () {
            return false;
        }

        function RowClick(currenttr, lock) {

            idSelectedRow = currenttr.getElementsByTagName("td")[1].innerHTML;
            console.log("idSelectedRow ",idSelectedRow)
            changedSelectedRow = true;
            indexDataReceived = 0;

            //drawChart();

            //Erase drawing
            data = new google.visualization.DataTable();


            if (window.event.ctrlKey) {
                //console.log("INGRESO control click", currenttr)
                toggleRow(currenttr);

                if(!(arraIdsSelects.includes(idSelectedRow))){
                    arraIdsSelects.push(idSelectedRow);

                }

                if (currenttr.className == ''){
                    
                    arraIdsSelects = arraIdsSelects.filter(e => e !== idSelectedRow);
                }
                
            }

            if (window.event.button === 0) {
                if (!window.event.ctrlKey) {
                    //console.log("INGRESO !window.event.ctrlKey")
                    clearAll();
                    toggleRow(currenttr);
                    arraIdsSelects = [];
                    arraIdsSelects.push(idSelectedRow);

                }

            }

            console.log("arraIdsSelects ", arraIdsSelects);
        }

        function toggleRow(row) {
            row.className = row.className == 'selected' ? '' : 'selected';
            lastSelectedRow = row;

        }

        function clearAll() {
            //var trs = document.getElementById('table').tBodies[0].getElementsByTagName('tr');
            var trs = document.getElementById('table').getElementsByTagName('tr');
            for (var i = 0; i < trs.length; i++) {
                trs[i].className = '';
            }
        }

