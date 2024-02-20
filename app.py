from flask import Flask, jsonify, request, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import joblib
from PIL import Image
import io

app = Flask(__name__)

model = load_model("./model_building/model.h5")
lightgbm_model = joblib.load("./model_building/lgb.pkl")


def preprocess(image, target_size=(225, 225)):
    img = Image.open(io.BytesIO(image))
    img = img.convert("RGB")
    img = img.resize(target_size)

    x = img_to_array(img)
    x = x.astype("float32") / 255
    x = np.expand_dims(x, axis=0)
    return x


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


if __name__ == "__main__":
    app.run(debug=True)
