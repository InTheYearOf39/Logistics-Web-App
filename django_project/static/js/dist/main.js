function draw_chartjs_chart(
  chart_type,
  canvas_id,
  x_values,
  datasets,
  chart_title,
  x_title,
  y_title
) {
  var ctx = document.getElementById(canvas_id).getContext("2d");
  var myChart = new Chart(ctx, {
    type: chart_type,
    data: {
      labels: x_values,
      datasets: datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      title: {
        display: true,
        text: chart_title,
      },
      scales: {
        x_axes: [
          {
            scaleLabel: {
              display: true,
              labelString: x_title,
            },
          },
        ],
        y_axes: [
          {
            scaleLabel: {
              display: true,
              labelString: y_title,
            },
            ticks: {
              beginAtZero: true,
              stepSize: 1, // Customize the step size as needed
            },
          },
        ],
      },
    },
  });
}
