'use strict';

var EnvironmentalDataChart = (function() {

  // Variables

  var $chart = $('#chart-environmental-data');

  // Methods

  function init($chart, data, labels) {

    var envDataChart = new Chart($chart, {
      type: 'line',
      options: {
        scales: {
          yAxes: [{
            gridLines: {
              lineWidth: 1,
              color: 'gray',
              zeroLineColor: 'gray'
            },
            ticks: {
              callback: function(value) {
                return value + '°C';
              }
            }
          }]
        },
        tooltips: {
          callbacks: {
            label: function(item, data) {
              var label = data.datasets[item.datasetIndex].label || '';
              var yLabel = item.yLabel;
              return label + ': ' + yLabel + '°C';
            }
          }
        }
      },
      data: {
        labels: labels,
        datasets: [{
          label: 'Temperature',
          data: data,
        }]
      }
    });

    $chart.data('chart', envDataChart);
  };

  if ($chart.length) {
    // Populate 'data' and 'labels' arrays with your temperature and humidity data and labels
    init($chart, data, labels);
  }

})();



function updateSensorData(chartInstance) {
  $.ajax({
      url: "/api/get_sensor_data/",
      method: "GET",
      success: function(response) {
          if(response.status === "success") {
              let newData = [];
              let newLabels = [];
              response.data.forEach((item) => {
                  newData.push(item.temperature);
                  newLabels.push(item.timestamp);
              });
              
              chartInstance.data.labels = newLabels;
              chartInstance.data.datasets[0].data = newData;
              chartInstance.update();
          }
      }
  });
}

// Assuming envDataChart is the Chart.js instance
$(document).ready(function () {
  setInterval(function() {
      updateSensorData(envDataChart);
  }, 60000);  // Update every 60 seconds
});


