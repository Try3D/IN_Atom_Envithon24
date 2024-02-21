const form = document.querySelector("form");

form.addEventListener("submit", (event) => {
  event.preventDefault();
  submitIrrigationForm();
});

function submitIrrigationForm() {
  let formData = new FormData(document.getElementById("irrigationForm"));

  fetch("/irrigation", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("result").innerHTML = `
          <p>Crop: ${data.crop}</p>
          <p>Status: ${data.status}</p>
          <p>Irrigation per day: ${data.toIrrigate} L/m²</p>
          `;
    });
}
