let ctx = document.getElementById("chart").getContext("2d");

let chart = new Chart(ctx, {
  type: "bar",
  data: {
     labels: [{% for order in object_list %}"{{order.marker}}",{% endfor %}],
     datasets: [
        {
          label: 'Сумма заказа',
          data: [{% for order in object_list %}{{order.total_price}},{% endfor %}],
          backgroundColor: "#79AEC8",
          borderColor: "#417690",
        }
     ]
  },
  options: {
     title: {
        text: "Gross Volume in 2020",
        display: true
     }
  }
});