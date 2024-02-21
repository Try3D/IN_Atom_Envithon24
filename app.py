from flask import Flask, jsonify, request, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import pandas as pd
import joblib
from PIL import Image
import io
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

df = pd.read_csv("./model_building/Food_Production.csv")
model = load_model("./model_building/model.h5")
lightgbm_model = joblib.load("./model_building/lgb.pkl")

apikey = "76e5a01f687342a8b3925619242102"
uri = "http://api.weatherapi.com/v1/"

df1 = df.dropna(
    subset=["Freshwater withdrawals per kilogram (liters per kilogram)"],
)


def preprocess(image, target_size=(225, 225)):
    img = Image.open(io.BytesIO(image))
    img = img.convert("RGB")
    img = img.resize(target_size)

    x = img_to_array(img)
    x = x.astype("float32") / 255
    x = np.expand_dims(x, axis=0)
    return x


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/detect", methods=["GET", "POST"])
def detect():
    if request.method == "GET":
        return render_template("detect.html")

    data = request.files["file"]
    image_blob = data.read()

    x = preprocess(image_blob, target_size=(225, 225))

    prediction = model.predict(x)
    labels = {0: "Healthy", 1: "Powdery", 2: "Rust"}
    pred_label = labels[np.argmax(prediction)]

    return jsonify({"prediction": pred_label})


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("predict.html")

    N = int(request.form.get("N"))
    P = int(request.form.get("P"))
    K = int(request.form.get("K"))
    temperature = float(request.form.get("temperature"))
    humidity = float(request.form.get("humidity"))
    ph = float(request.form.get("ph"))

    input_array = np.array([N, P, K, temperature, humidity, ph]).reshape(1, -1)
    prediction = lightgbm_model.predict(input_array)[0]

    return jsonify({"prediction": prediction})


@app.route("/irrigation", methods=["GET", "POST"])
def irrigation():
    if request.method == "GET":
        crops = df["Food product"].tolist()
        return render_template("irrigation.html", crops=crops)

    crop = request.form.get("crop")
    irrigation = float(request.form.get("irrigation"))

    to_irrigate = df.loc[df["Food product"] == crop][
        "Freshwater withdrawals per kilogram (liters per kilogram)"
    ].tolist()[0]
    to_irrigate_daily = to_irrigate / 365
    delta = to_irrigate_daily / 10

    status = ""
    if irrigation - to_irrigate_daily > delta:
        status = "You are over irrigating."
    elif irrigation - to_irrigate_daily < -delta:
        status = "You are under irrigating."
    else:
        status = "You are irrigating correctly."

    return jsonify(
        {
            "crop": f"{ crop }",
            "status": f"{ status }",
            "toIrrigate": f"{to_irrigate_daily}",
        }
    )


def get_date(date):
    return (
        f"{str(date.year).zfill(2)}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)}"
    )


@app.route("/location", methods=["GET", "POST"])
def location():
    if request.method == "GET":
        return render_template("location.html")

    latitude = float(request.form.get("latitude"))
    longitude = float(request.form.get("longitude"))

    now = datetime.now()
    monthfromnow = now + timedelta(days=30)
    month_6fromnow = now + timedelta(days=180)

    cur = requests.get(
        f"{uri}forecast.json?key={apikey}&q={latitude},{longitude}&days=7"
    )

    month = requests.get(
        f"{uri}future.json?key={apikey}&q={latitude},{longitude}&dt={get_date(monthfromnow)}"
    )

    month_6 = requests.get(
        f"{uri}future.json?key={apikey}&q={latitude},{longitude}&dt={get_date(month_6fromnow)}"
    )

    return {
        "cur": cur.json(),
        "month": month.json(),
        "month_6": month_6.json(),
    }


if __name__ == "__main__":
    app.run(debug=True)
