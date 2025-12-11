function updateCharts() {
  $.getJSON("/data", function(data) {
    let timestamps = data.map(d => new Date(d[0]));
    let charts = [
      {id: 'temp_chart', data: data.map(d => d[1])},
      {id: 'hum_chart', data: data.map(d => d[2])},
      {id: 'powcun_chart', data: data.map(d => d[3])},
      {id: 'pressure_chart', data: data.map(d => d[4])},
      {id: 'material_flow_chart', data: data.map(d => d[5])},
      {id: 'cycle_time_chart', data: data.map(d => d[6])},
      {id: 'error_rate_chart', data: data.map(d => d[7])},
      {id: 'downtime_chart', data: data.map(d => d[8])},
      {id: 'maintenance_flag_chart', data: data.map(d => d[9])},
      {id: 'efficiency_score_chart', data: data.map(d => d[10])},
      {id: 'production_status_chart', data: data.map(d => d[11])},
    ];

    charts.forEach(c => {
      Plotly.newPlot(c.id, [{
        x: timestamps,
        y: c.data,
        type: 'scatter',
        mode: 'markers',   // ✅ only points
        marker: { color: 'red', size: 6 }
      }], {
        margin: { t: 20 },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: 'white' }
      }, {displayModeBar: false}); // ✅ hide toolbar
    });
  });
}

function showChart(chartId) {
  let charts = document.querySelectorAll(".chart");

  if (chartId === "all") {
    charts.forEach(c => {
      c.style.display = "block";
      c.style.opacity = 0;
      setTimeout(() => (c.style.opacity = 1), 100);
    });
  } else {
    charts.forEach(c => {
      if (c.querySelector("div").id === chartId) {
        c.style.display = "block";
        c.style.opacity = 0;
        setTimeout(() => (c.style.opacity = 1), 100);
      } else {
        c.style.display = "none";
      }
    });
  }
}

// Initial render
updateCharts();

// Auto refresh every 0.5 seconds
setInterval(updateCharts, 500);

function loadLatestValues() {
    $.get('/data', function(response) {
        if (!response || response.length === 0) return;

        // Response array: [created_at, temperature, humidity, vibration, flow, voltage]
        let latest = response[response.length - 1];

        $("#box_temperature").text(latest[1]);
        $("#box_humidity").text(latest[2]);
        $("#box_vibration").text(latest[3]);
        $("#box_flow").text(latest[4]);
        $("#box_voltage").text(latest[5]);
    });
}

// Load on start
loadLatestValues();

// Auto-refresh every 0.5 seconds
setInterval(loadLatestValues, 500);


// === AUTO LOAD LIVE VALUES + TABLE + STATS ===

function loadAllData() {
    $.get('/data', function(response) {

        if (!response || response.length === 0) return;

        // The entire table data
        let data = response;

        // === 1. UPDATE TOP BOXES (latest row) ===
        let latest = data[data.length - 1]; 
        $("#box_temperature").text(latest[1]);
        $("#box_humidity").text(latest[2]);
        $("#box_vibration").text(latest[3]);
        $("#box_flow").text(latest[4]);
        $("#box_voltage").text(latest[5]);

        // === 2. UPDATE TABLE ===
        let tableBody = $("#table_body");
        tableBody.empty(); // clear old rows

        data.forEach(row => {
            let tr = "<tr>";
            row.forEach(cell => {
                tr += `<td>${cell}</td>`;
            });
            tr += "</tr>";
            tableBody.append(tr);
        });

        // === 3. UPDATE STATISTICS ===
        calculateStats(data);
    });
}

// === STATS FUNCTION ===
function calculateStats(data) {

    const TEMP = 1, HUM = 2, VIB = 3, FLOW = 4, VOLT = 5;

    function extract(col) { return data.map(r => Number(r[col])); }
    function min(arr) { return Math.min(...arr); }
    function max(arr) { return Math.max(...arr); }
    function mean(arr) { return (arr.reduce((a,b) => a + b, 0) / arr.length).toFixed(2); }
    function runningAvg(arr, count = 10) {
        let slice = arr.slice(-count);
        return mean(slice);
    }

    // Temperature
    let t = extract(TEMP);
    $("#temp_min").text(min(t));
    $("#temp_max").text(max(t));
    $("#temp_mean").text(mean(t));
    $("#temp_run").text(runningAvg(t));

    // Humidity
    let h = extract(HUM);
    $("#hum_min").text(min(h));
    $("#hum_max").text(max(h));
    $("#hum_mean").text(mean(h));
    $("#hum_run").text(runningAvg(h));

    // Vibration
    let v = extract(VIB);
    $("#vib_min").text(min(v));
    $("#vib_max").text(max(v));
    $("#vib_mean").text(mean(v));
    $("#vib_run").text(runningAvg(v));

    // Flow
    let f = extract(FLOW);
    $("#flow_min").text(min(f));
    $("#flow_max").text(max(f));
    $("#flow_mean").text(mean(f));
    $("#flow_run").text(runningAvg(f));

    // Voltage
    let vlt = extract(VOLT);
    $("#volt_min").text(min(vlt));
    $("#volt_max").text(max(vlt));
    $("#volt_mean").text(mean(vlt));
    $("#volt_run").text(runningAvg(vlt));
}

// === AUTO REFRESH EVERY 1 SECOND ===
loadAllData();
setInterval(loadAllData, 1000);
