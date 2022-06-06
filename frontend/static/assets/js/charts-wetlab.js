$(function () {
  // https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
  // EXTRACTION CHARTS
  // line chart
  var $chartExtractionCount = $("#chartExtractionCount");
  var $extractionTotal = $("#extractionTotal");
  var $lastExtractionDate = $('#lastExtractionDate');
  var $chartExtractionCountLoading = $('#chartExtractionCountLoading');
  var $chartExtractionCountEmpty = $('#chartExtractionCountEmpty');
  $.ajax({
    url: $chartExtractionCount.data("url"),
    success: function (data) {
        //console.log(data.data.length)
        if (!Array.isArray(data.data) == undefined || !data.data.length) {
            var extractionSum = 0;
            $extractionTotal.text(extractionSum);
            $chartExtractionCountLoading.remove();
            $chartExtractionCount.remove();
            $lastExtractionDate.text("No extractions.");
            $chartExtractionCountEmpty.text("There are 0 extractions.");
        } else {
            var extractionSum = data.data.reduce((partialSum, a) => partialSum + a, 0);
            var lastExtraction = data.labels.slice(-1)[0];
            //console.log(surveySum);
            $extractionTotal.text(extractionSum);
            $lastExtractionDate.text(lastExtraction);
            $chartExtractionCountLoading.remove();
            $chartExtractionCountEmpty.remove();
            var wlCtx1 = $chartExtractionCount[0].getContext("2d");
            new Chart(wlCtx1, {
              type: "line",
              data: {
                labels: data.labels,
                datasets: [{
                    label: "Extraction Count",
                    tension: 0.4,
                    borderWidth: 0,
                    pointRadius: 2,
                    pointBackgroundColor: "#e3316e",
                    borderColor: "#e3316e",
                    borderWidth: 3,
                    backgroundColor: 'transparent',
                    data: data.data,
                    maxBarThickness: 6
                  }],
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    display: false,
                  }
                },
                interaction: {
                  intersect: false,
                  mode: 'index',
                },
                scales: {
                  y: {
                    grid: {
                      drawBorder: false,
                      display: true,
                      drawOnChartArea: true,
                      drawTicks: false,
                      borderDash: [5, 5]
                    },
                    ticks: {
                      display: true,
                      padding: 10,
                      color: '#b2b9bf',
                      font: {
                        size: 11,
                        family: "Open Sans",
                        style: 'normal',
                        lineHeight: 2
                      },
                    }
                  },
                  x: {
                    grid: {
                      drawBorder: false,
                      display: true,
                      drawOnChartArea: true,
                      drawTicks: true,
                      borderDash: [5, 5]
                    },
                    ticks: {
                      display: true,
                      color: '#b2b9bf',
                      padding: 10,
                      font: {
                        size: 11,
                        family: "Open Sans",
                        style: 'normal',
                        lineHeight: 2
                      },
                    }
                  },
                },
              },
            });
        }

    }
  });

  // RUN RESULT CHARTS
  // line chart
  var $chartRunResultCount = $("#chartRunResultCount");
  var $runResultTotal = $("#runResultTotal");
  var $lastRunResultDate = $('#lastRunResultDate');
  var $chartRunResultCountLoading = $('#chartRunResultCountLoading');
  var $chartRunResultCountEmpty = $('#chartRunResultCountEmpty');
  $.ajax({
    url: $chartRunResultCount.data("url"),
    success: function (data) {
        //console.log(data.data.length)
        if (!Array.isArray(data.data) == undefined || !data.data.length) {
            var runResultSum = 0;
            $runResultTotal.text(runResultSum);
            $chartRunResultCount.remove();
            $chartRunResultCountLoading.remove();
            $lastRunResultDate.text("No run results.");
            $chartRunResultCountEmpty.text("There are 0 run results.");
        } else {
            var runResultSum = data.data.reduce((partialSum, a) => partialSum + a, 0);
            var lastRunResult = data.labels.slice(-1)[0];
            //console.log(surveySum);
            $runResultTotal.text(runResultSum);
            $lastRunResultDate.text(lastRunResult);
            $chartRunResultCountLoading.remove();
            $chartRunResultCountEmpty.remove();
            var wlCtx2 = $chartRunResultCount[0].getContext("2d");
            new Chart(wlCtx2, {
              type: "line",
              data: {
                labels: data.labels,
                datasets: [{
                    label: "Run Count",
                    tension: 0.4,
                    borderWidth: 0,
                    pointRadius: 2,
                    pointBackgroundColor: "#e3316e",
                    borderColor: "#e3316e",
                    borderWidth: 3,
                    backgroundColor: 'transparent',
                    data: data.data,
                    maxBarThickness: 6
                  }],
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    display: false,
                  }
                },
                interaction: {
                  intersect: false,
                  mode: 'index',
                },
                scales: {
                  y: {
                    grid: {
                      drawBorder: false,
                      display: true,
                      drawOnChartArea: true,
                      drawTicks: false,
                      borderDash: [5, 5]
                    },
                    ticks: {
                      display: true,
                      padding: 10,
                      color: '#b2b9bf',
                      font: {
                        size: 11,
                        family: "Open Sans",
                        style: 'normal',
                        lineHeight: 2
                      },
                    }
                  },
                  x: {
                    grid: {
                      drawBorder: false,
                      display: true,
                      drawOnChartArea: true,
                      drawTicks: true,
                      borderDash: [5, 5]
                    },
                    ticks: {
                      display: true,
                      color: '#b2b9bf',
                      padding: 10,
                      font: {
                        size: 11,
                        family: "Open Sans",
                        style: 'normal',
                        lineHeight: 2
                      },
                    }
                  },
                },
              },
            });
        }

    }
  });

});