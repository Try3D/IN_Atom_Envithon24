document.querySelector("form").addEventListener("submit", uploadFile);

function uploadFile(e) {
  e.preventDefault();
  let formData = new FormData(document.getElementById("uploadForm"));

  fetch("/detect", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("result").innerHTML =
        "<p>Prediction: " + data.prediction + "</p>";
    })
    .catch((error) => console.error("Error:", error));
}
