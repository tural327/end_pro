// === 1) UPDATE CHARTS ===
function updateCharts() {
  $.getJSON("/data_sistem2", function(data) {
    if (!data || data.length === 0) return;

    let timestamps = data.map(d => new Date(d[0]));

    let charts = [
      { id: 'p1_chart', data: data.map(d => d[1]) },
      { id: 'p2_chart', data: data.map(d => d[2]) },
      { id: 'p3_chart', data: data.map(d => d[3]) },
      { id: 'p4_chart', data: data.map(d => d[4]) },
      { id: 'p5_chart', data: data.map(d => d[5]) }
    ];

    charts.forEach(c => {
      Plotly.newPlot(
        c.id,
        [
          {
            x: timestamps,
            y: c.data,
            type: 'scatter',
            mode: 'markers',
            marker: { color: 'red', size: 6 }
          }
        ],
        {
          margin: { t: 20 },
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          font: { color: 'white' }
        },
        { displayModeBar: false }
      );
    });
  });
}

// Show/Hide charts
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

updateCharts();
setInterval(updateCharts, 1000);


// === 2) LATEST VALUES (TOP BOXES) ===
function loadLatestValues() {
  $.get('/data_sistem2', function(response) {
    if (!response || response.length === 0) return;

    let latest = response[response.length - 1];

    $("#box_temperature").text(latest[1]);
    $("#box_humidity").text(latest[2]);
    $("#box_vibration").text(latest[3]);
    $("#box_flow").text(latest[4]);
    $("#box_voltage").text(latest[5]);
  });
}

loadLatestValues();
setInterval(loadLatestValues, 1000);


// === 3) LOAD ALL DATA (TABLE + STATS) ===
function loadAllData() {
  $.get('/data_sistem2', function(response) {
    if (!response || response.length === 0) return;

    let data = response;

    // --- update top boxes ---
    let latest = data[data.length - 1];
    $("#box_temperature").text(latest[1]);
    $("#box_humidity").text(latest[2]);
    $("#box_vibration").text(latest[3]);
    $("#box_flow").text(latest[4]);
    $("#box_voltage").text(latest[5]);

    // --- update table rows ---
    let tableBody = $("#table_body");
    tableBody.empty();

    data.forEach(row => {
      let tr = "<tr>";
      row.forEach(cell => {
        tr += `<td>${cell}</td>`;
      });
      tr += "</tr>";
      tableBody.append(tr);
    });

    // --- update statistics ---
    calculateStats(data);
  });
}

loadAllData();
setInterval(loadAllData, 1000);


// === 4) STATISTICS ===
function calculateStats(data) {
  const P1 = 1, P2 = 2, P3 = 3, P4 = 4, P5 = 5;

  function extract(col) { return data.map(r => Number(r[col])); }
  function min(arr) { return Math.min(...arr); }
  function max(arr) { return Math.max(...arr); }
  function mean(arr) { return (arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(2); }
  function runningAvg(arr, count = 10) {
    let slice = arr.slice(-count);
    return mean(slice);
  }

  // P1
  let p1 = extract(P1);
  $("#temp_min").text(min(p1));
  $("#temp_max").text(max(p1));
  $("#temp_mean").text(mean(p1));
  $("#temp_run").text(runningAvg(p1));

  // P2
  let p2 = extract(P2);
  $("#hum_min").text(min(p2));
  $("#hum_max").text(max(p2));
  $("#hum_mean").text(mean(p2));
  $("#hum_run").text(runningAvg(p2));

  // P3
  let p3 = extract(P3);
  $("#vib_min").text(min(p3));
  $("#vib_max").text(max(p3));
  $("#vib_mean").text(mean(p3));
  $("#vib_run").text(runningAvg(p3));

  // P4
  let p4 = extract(P4);
  $("#flow_min").text(min(p4));
  $("#flow_max").text(max(p4));
  $("#flow_mean").text(mean(p4));
  $("#flow_run").text(runningAvg(p4));

  // P5
  let p5 = extract(P5);
  $("#volt_min").text(min(p5));
  $("#volt_max").text(max(p5));
  $("#volt_mean").text(mean(p5));
  $("#volt_run").text(runningAvg(p5));
}
