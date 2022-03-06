$(function () {
    // https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    //var json_data = document.getElementById('survey-count-data').textContent;
    // the information in this tag is no longer being used, so remove the content from the page
    //document.getElementById('survey_count').remove()

    //console.log(json_data)
    //console.log(survey_count)

  // SURVEY CHARTS
  // line chart
  var $chartSurveyCount = $("#chartSurveyCount");
  var $surveyTotal = $("#surveyTotal");
  $.ajax({
    url: $chartSurveyCount.data("url"),
    success: function (data) {
        if (!Array.isArray(data.data) == undefined || !data.data.length) {
            var surveySum = 0;
            $surveyTotal.text(surveySum);
            var fsCtx1 = $chartSurveyCount[0].getContext("2d");
            fsCtx1.fillStyle = "black";
            fsCtx1.font = "bold 18px Arial";
            fsCtx1.fillText("There are 0 surveys.", ($chartSurveyCount.width / 2) - 17, ($chartSurveyCount.height / 2) + 8);
        } else {
            var surveySum = data.data.reduce((partialSum, a) => partialSum + a, 0);
            //console.log(surveySum);
            $surveyTotal.text(surveySum);
            var fsCtx1 = $chartSurveyCount[0].getContext("2d");
            new Chart(fsCtx1, {
              type: "line",
              data: {
                labels: data.labels,
                datasets: [{
                    label: "Survey Count",
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

  // bar chart
  var $chartSurveySiteCount = $("#chartSurveySiteCount");
  $.ajax({
    url: $chartSurveySiteCount.data("url"),
    success: function (data) {
        if (!Array.isArray(data.data) == undefined || !data.data.length) {
            var fsCtx2 = $chartSurveySiteCount[0].getContext("2d");
            fsCtx2.fillStyle = "black";
            fsCtx2.font = "bold 18px Arial";
            fsCtx2.fillText("There are 0 surveys.", ($chartSurveySiteCount.width / 2) - 17, ($chartSurveySiteCount.height / 2) + 8);
        } else {
            var fsCtx2 = $chartSurveySiteCount[0].getContext("2d");
            new Chart(fsCtx2, {
            type: "bar",
            data: {
              labels: data.labels,
              datasets: [{
                label: "Surveys by Site",
                weight: 5,
                borderWidth: 0,
                borderRadius: 4,
                backgroundColor: '#3A416F',
                data: data.data,
                fill: false,
                maxBarThickness: 35
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
                    color: '#9ca2b7'
                  }
                },
                x: {
                  grid: {
                    drawBorder: false,
                    display: false,
                    drawOnChartArea: true,
                    drawTicks: true,
                  },
                  ticks: {
                    display: true,
                    color: '#9ca2b7',
                    padding: 10
                  }
                },
              },
            },
            });
        }

      }
    });

  // Pie chart
  var $chartSurveySystemCount = $("#chartSurveySystemCount");
  $.ajax({
    url: $chartSurveySystemCount.data("url"),
    success: function (data) {
        if (!Array.isArray(data.data) == undefined || !data.data.length) {
            var fsCtx3 = $chartSurveySystemCount[0].getContext("2d");
            fsCtx3.fillStyle = "black";
            fsCtx3.font = "bold 18px Arial";
            fsCtx3.fillText("There are 0 surveys.", ($chartSurveySystemCount.width / 2) - 17, ($chartSurveySystemCount.height / 2) + 8);
        } else {
            var colors = palette(['tol', 'qualitative'], data.labels.length)
            colors = colors.map(i => '#' + i);
            var fsCtx3 = $chartSurveySystemCount[0].getContext("2d");
            new Chart(fsCtx3, {
              type: "pie",
              data: {
                labels: data.labels,
                datasets: [{
                  label: "Survey Count",
                  weight: 9,
                  cutout: 0,
                  tension: 0.9,
                  pointRadius: 2,
                  borderWidth: 2,
                  backgroundColor: colors,
                  data: data.data,
                  fill: false
                }],
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    position: 'left',
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
                      display: false,
                      drawOnChartArea: false,
                      drawTicks: false,
                    },
                    ticks: {
                      display: false
                    }
                  },
                  x: {
                    grid: {
                      drawBorder: false,
                      display: false,
                      drawOnChartArea: false,
                      drawTicks: false,
                    },
                    ticks: {
                      display: false,
                    }
                  },
                },
              },
            });
           }
    }
  });

  // Field Sample CHARTS
  // line chart
  var $chartFieldSampleCount = $("#chartFieldSampleCount");
  var $fieldSampleTotal = $("#fieldSampleTotal");
  var $filterTotal = $("#filterTotal");
  var $subCoreTotal = $("#subCoreTotal");
  $.ajax({
    url: $chartFieldSampleCount.data("url"),
    success: function (data) {
        if (!Array.isArray(data.fieldsample_data) == undefined || !data.fieldsample_data.length) {
            var fieldSampleSum = 0;
            var filterSum = 0;
            var subCoreSum = 0;
            $fieldSampleTotal.text(fieldSampleSum);
            $filterTotal.text(filterSum);
            $subCoreTotal.text(subCoreSum);
            var fsCtx4 = $chartFieldSampleCount[0].getContext("2d");
            fsCtx4.fillStyle = "black";
            fsCtx4.font = "bold 18px Arial";
            fsCtx4.fillText("There are 0 field samples.", ($chartFieldSampleCount.width / 2) - 17, ($chartFieldSampleCount.height / 2) + 8);
        } else {
            var fieldSampleSum = data.fieldsample_data.reduce((partialSum, a) => partialSum + a, 0);
            var filterSum = data.filter_data.reduce((partialSum, a) => partialSum + a, 0);
            var subCoreSum = data.subcore_data.reduce((partialSum, a) => partialSum + a, 0);
            //console.log(surveySum);
            $fieldSampleTotal.text(fieldSampleSum);
            $filterTotal.text(filterSum);
            $subCoreTotal.text(subCoreSum);
            var fsCtx4 = $chartFieldSampleCount[0].getContext("2d");
            new Chart(fsCtx4, {
              type: "line",
              data: {
                labels: data.count_labels,
                datasets: [{
                    label: "Filter Count",
                    tension: 0.4,
                    borderWidth: 0,
                    pointRadius: 2,
                    pointBackgroundColor: "#e3316e",
                    borderColor: "#e3316e",
                    borderWidth: 3,
                    backgroundColor: 'transparent',
                    data: data.filter_data,
                    maxBarThickness: 6
                  },
                  {
                    label: "SubCore Count",
                    tension: 0.4,
                    borderWidth: 0,
                    pointRadius: 2,
                    pointBackgroundColor: "#3A416F",
                    borderColor: "#3A416F",
                    borderWidth: 3,
                    backgroundColor: 'transparent',
                    data: data.subcore_data,
                    maxBarThickness: 6
                  },

                ],
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

  // Pie chart
  var $chartFilterTypeCount = $("#chartFilterTypeCount");
  $.ajax({
    url: $chartFilterTypeCount.data("url"),
    success: function (data) {
        if (!Array.isArray(data.data) == undefined || !data.data.length) {
            var fsCtx5 = $chartFilterTypeCount[0].getContext("2d");
            fsCtx5.fillStyle = "black";
            fsCtx5.font = "bold 18px Arial";
            fsCtx5.fillText("There are 0 filters.", ($chartFilterTypeCount.width / 2) - 17, ($chartFilterTypeCount.height / 2) + 8);
        } else {
            var colors = palette(['tol', 'qualitative'], data.labels.length)
            colors = colors.map(i => '#' + i);
            var fsCtx5 = $chartFilterTypeCount[0].getContext("2d");
            new Chart(fsCtx5, {
              type: "pie",
              data: {
                labels: data.labels,
                datasets: [{
                  label: "Filter Count",
                  weight: 9,
                  cutout: 0,
                  tension: 0.9,
                  pointRadius: 2,
                  borderWidth: 2,
                  backgroundColor: colors,
                  data: data.data,
                  fill: false
                }],
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    position: 'left',
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
                      display: false,
                      drawOnChartArea: false,
                      drawTicks: false,
                    },
                    ticks: {
                      display: false
                    }
                  },
                  x: {
                    grid: {
                      drawBorder: false,
                      display: false,
                      drawOnChartArea: false,
                      drawTicks: false,
                    },
                    ticks: {
                      display: false,
                    }
                  },
                },
              },
            });

        }
    }
  });

  // bar chart
  var $chartFilterSiteCount = $("#chartFilterSiteCount");
  $.ajax({
    url: $chartFilterSiteCount.data("url"),
    success: function (data) {
        if (!Array.isArray(data.data) == undefined || !data.data.length) {
            var fsCtx6 = $chartFilterSiteCount[0].getContext("2d");
            fsCtx6.fillStyle = "black";
            fsCtx6.font = "bold 18px Arial";
            fsCtx6.fillText("There are 0 filters.", ($chartFilterSiteCount.width / 2) - 17, ($chartFilterSiteCount.height / 2) + 8);
        } else {
            var fsCtx6 = $chartFilterSiteCount[0].getContext("2d");
            new Chart(fsCtx6, {
            type: "bar",
            data: {
              labels: data.labels,
              datasets: [{
                label: "Filters by Site",
                weight: 5,
                borderWidth: 0,
                borderRadius: 4,
                backgroundColor: '#3A416F',
                data: data.data,
                fill: false,
                maxBarThickness: 35
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
                    color: '#9ca2b7'
                  }
                },
                x: {
                  grid: {
                    drawBorder: false,
                    display: false,
                    drawOnChartArea: true,
                    drawTicks: true,
                  },
                  ticks: {
                    display: true,
                    color: '#9ca2b7',
                    padding: 10
                  }
                },
              },
            },
          });
        }

    }
  });

  // Pie chart
  var $chartFilterSystemCount = $("#chartFilterSystemCount");
  $.ajax({
    url: $chartFilterSystemCount.data("url"),
    success: function (data) {
        if (!Array.isArray(data.data) == undefined || !data.data.length) {
            var fsCtx7 = $chartFilterSystemCount[0].getContext("2d");
            fsCtx7.fillStyle = "black";
            fsCtx7.font = "bold 18px Arial";
            fsCtx7.fillText("There are 0 filters.", ($chartFilterSystemCount.width / 2) - 17, ($chartFilterSystemCount.height / 2) + 8);
        } else {
            var colors = palette(['tol', 'qualitative'], data.labels.length)
            colors = colors.map(i => '#' + i);
            var fsCtx7 = $chartFilterSystemCount[0].getContext("2d");
            new Chart(fsCtx7, {
              type: "pie",
              data: {
                labels: data.labels,
                datasets: [{
                  label: "Survey Count",
                  weight: 9,
                  cutout: 0,
                  tension: 0.9,
                  pointRadius: 2,
                  borderWidth: 2,
                  backgroundColor: colors,
                  data: data.data,
                  fill: false
                }],
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    position: 'left',
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
                      display: false,
                      drawOnChartArea: false,
                      drawTicks: false,
                    },
                    ticks: {
                      display: false
                    }
                  },
                  x: {
                    grid: {
                      drawBorder: false,
                      display: false,
                      drawOnChartArea: false,
                      drawTicks: false,
                    },
                    ticks: {
                      display: false,
                    }
                  },
                },
              },
            });
        }

    }
  });

});