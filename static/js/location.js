document.querySelector("form").addEventListener("submit", submit);

document.getElementById("geolocation").addEventListener("click", function () {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
      const latitude = position.coords.latitude;
      const longitude = position.coords.longitude;
      document.getElementById("latitude").value = latitude;
      document.getElementById("longitude").value = longitude;
      document.getElementById("response").innerHTML = "Loading...";

      let formData = new FormData(document.querySelector("form"));

      submit(null, formData);
    });
  }
});

function submit(e) {
  e?.preventDefault();

  document.getElementById("response").innerHTML = "Loading...";

  let formData = new FormData(document.querySelector("form"));

  fetch("/location", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("response").innerHTML = `
      <div><b>Location:</b> ${data.cur.location.name}, ${data.cur.location.region}</div>
      <div><b>Country:</b> ${data.cur.location.country}</div>
      <div><b>LocalTime:</b> ${data.cur.location.localtime}</div>
      <div><b>Location:</b> ${data.cur.location.lat}, ${data.cur.location.lon}</div>
      <table class="table">
        <thead>
          <tr>
            <th>When</th>
            <th>Desc </th>
            <th>Temperature (°C)</th>
            <th>Wind (Kph)</th>
            <th>Humidity (%</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Now</td>
            <td>${data.cur.current.condition.text}</td>
            <td>${data.cur.current.temp_c}</td>
            <td>${data.cur.current.gust_kph}</td>
            <td>${data.cur.current.humidity}</td>
          </tr>
          <tr>
            <td>Today</td>
            <td>${data.cur.forecast.forecastday[0].day.condition.text}</td>
            <td>${data.cur.forecast.forecastday[0].day.avgtemp_c}</td>
            <td>${data.cur.forecast.forecastday[0].day.maxwind_kph}</td>
            <td>${data.cur.forecast.forecastday[0].day.avghumidity}</td>
          </tr>
          <tr>
            <td>Tomorrow</td>
            <td>${data.cur.forecast.forecastday[1].day.condition.text}</td>
            <td>${data.cur.forecast.forecastday[1].day.avgtemp_c}</td>
            <td>${data.cur.forecast.forecastday[1].day.maxwind_kph}</td>
            <td>${data.cur.forecast.forecastday[1].day.avghumidity}</td>
          </tr>
          <tr>
            <td>Day after Tomorrow</td>
            <td>${data.cur.forecast.forecastday[2].day.condition.text}</td>
            <td>${data.cur.forecast.forecastday[2].day.avgtemp_c}</td>
            <td>${data.cur.forecast.forecastday[2].day.maxwind_kph}</td>
            <td>${data.cur.forecast.forecastday[2].day.avghumidity}</td>
          </tr>
          <tr>
            <td>Next week</td>
            <td>${data.cur.forecast.forecastday[6].day.condition.text}</td>
            <td>${data.cur.forecast.forecastday[6].day.avgtemp_c}</td>
            <td>${data.cur.forecast.forecastday[6].day.maxwind_kph}</td>
            <td>${data.cur.forecast.forecastday[6].day.avghumidity}</td>
          </tr>
          <tr>
            <td>Next month</td>
            <td>${data.month.forecast.forecastday[0].day.condition.text}</td>
            <td>${data.month.forecast.forecastday[0].day.avgtemp_c}</td>
            <td>${data.month.forecast.forecastday[0].day.maxwind_kph}</td>
            <td>${data.month.forecast.forecastday[0].day.avghumidity}</td>
          </tr>
          <tr>
            <td>6 months</td>
            <td>${data.month_6.forecast.forecastday[0].day.condition.text}</td>
            <td>${data.month_6.forecast.forecastday[0].day.avgtemp_c}</td>
            <td>${data.month_6.forecast.forecastday[0].day.maxwind_kph}</td>
            <td>${data.month_6.forecast.forecastday[0].day.avghumidity}</td>
          </tr>
        </tbody>
      `;
    })
    .catch((error) => {
      console.error("Error submitting form:", error);
      document.getElementById("response").innerHTML =
        "An error occurred while submitting the form.";
    });
}
