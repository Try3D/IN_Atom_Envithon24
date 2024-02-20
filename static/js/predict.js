const form = document.getElementById("cropForm");

document.querySelector("form").addEventListener("submit", predictCrop);

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function predictCrop(e) {
  e.preventDefault();
  let formData = new FormData(form);

  fetch("/predict", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("result-container").innerHTML =
        "<p>Prediction: " + capitalizeFirstLetter(data.prediction) + "</p>";
    });
}
