from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)

# ---------------- LOAD MODEL ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "aqi_model.pkl")

# Load model safely
try:
    model = pickle.load(open(model_path, "rb"))
    print("✅ Model loaded successfully")
except:
    model = None
    print("⚠️ Model not found. Prediction disabled.")

# ---------------- AQI INFO FUNCTION ----------------
def aqi_info(aqi):
    if 0 <= aqi <= 50:
        return "Good", "Air quality is satisfactory; no risk.", "green"
    elif aqi <= 100:
        return "Moderate", "Sensitive people should be careful.", "yellow"
    elif aqi <= 150:
        return "Unhealthy (Sensitive)", "Limit outdoor activity.", "orange"
    elif aqi <= 200:
        return "Unhealthy", "Health effects possible.", "red"
    elif aqi <= 300:
        return "Very Unhealthy", "Serious health effects.", "purple"
    else:
        return "Hazardous", "Avoid outdoor activity.", "maroon"

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- ARCHITECTURE ----------------
@app.route("/architecture")
def architecture():
    return render_template("architecture.html")

# ---------------- WHAT IS MY PROJECT ----------------
@app.route("/project")
def project():
    return render_template("project.html")

# ---------------- DEVELOPER PROFILE ----------------
@app.route("/developer")
def developer():
    return render_template("developer.html")

# ---------------- PREDICT PAGE ----------------
@app.route("/visualization")
def visualization():
    return render_template("visualization.html")

# ---------------- PREDICT PAGE ----------------
@app.route("/prediction", methods=["GET", "POST"])
@app.route("/predict", methods=["GET", "POST"])
def predict():

    data_out = None
    error = None

    if request.method == "POST":

        if model is None:
            error = "Model not loaded."
            return render_template("prediction.html", error=error)

        try:
            lat = float(request.form.get("lat"))
            lon = float(request.form.get("lon"))
            pm25 = float(request.form.get("pm25"))
            pm10 = float(request.form.get("pm10"))
            no2 = float(request.form.get("no2"))
            o3 = float(request.form.get("o3"))

            X = np.array([[lat, lon, pm25, pm10, no2, o3]])

            predicted = float(model.predict(X)[0])

            category, advice, color = aqi_info(predicted)

            data_out = {
                "aqi": round(predicted, 2),
                "category": category,
                "advice": advice,
                "color": color,
                "lat": lat,
                "lon": lon,
                "pm25": pm25,
                "pm10": pm10,
                "no2": no2,
                "o3": o3
            }

        except Exception as e:
            print("ERROR:", e)
            error = "Invalid input. Please enter valid numbers."

    return render_template("prediction.html", data=data_out, error=error)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)