$(function () {
    // https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html

  // EXTRACTION CHARTS
  // line chart
  var $chartExtractionCount = $("#chartExtractionCount");
  var $extractionTotal = $("#extractionTotal");
  $.ajax({
    url: $chartExtractionCount.data("url"),
    success: function (data) {
        //console.log(data.data.length)
        if (!Array.isArray(data.data) == undefined || !data.data.length) {
            var extractionSum = 0;
            $extractionTotal.text(extractionSum);
            var wlCtx1 = $chartExtractionCount[0].getContext("2d");
            wlCtx1.fillStyle = "black";
            wlCtx1.font = "bold 18px Arial";
            wlCtx1.fillText("There are 0 extractions.", ($chartExtractionCount.width / 2) - 17, ($chartExtractionCount.height / 2) + 8);
        } else {
            var extractionSum = data.data.reduce((partialSum, a) => partialSum + a, 0);
            //console.log(surveySum);
            $extractionTotal.text(extractionSum);
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


});