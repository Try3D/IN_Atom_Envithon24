from flask import Flask, jsonify, request, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

model = load_model("./model_building/model.h5")


def preprocess(image, target_size=(225, 225)):
    img = Image.open(io.BytesIO(image))
    img = img.convert("RGB")
    img = img.resize(target_size)

    x = img_to_array(img)
    x = x.astype("float32") / 255
    x = np.expand_dims(x, axis=0)
    return x


@app.route("/detect")
def index():
    return render_template("detect.html")


@app.route("/detect", methods=["POST"])
def detect():
    data = request.files["file"]
    image_blob = data.read()
    x = preprocess(image_blob, target_size=(225, 225))
    prediction = model.predict(x)
    labels = {0: "Healthy", 1: "Powdery", 2: "Rust"}
    pred_label = labels[np.argmax(prediction)]
    return jsonify({"prediction": pred_label})


if __name__ == "__main__":
    app.run(debug=True)
