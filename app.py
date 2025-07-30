import pickle
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def home():
    prediction_text = None
    user_input = {}
    if request.method == "POST":
        try:
            gender = int(request.form["gender"])
            hemoglobin = float(request.form["hemoglobin"])
            # Add more fields if your model uses them, e.g.:
            # mch = float(request.form["mch"])
            # mcv = float(request.form["mcv"])
            # mchc = float(request.form["mchc"])
            # features = np.array([[gender, hemoglobin, mch, mcv, mchc]])
            features = np.array([[gender, hemoglobin]])
            prediction = model.predict(features)[0]
            prediction_text = "🩸 <b>You have Anemia.</b>" if int(prediction) == 1 else "✅ <b>You do not have Anemia.</b>"
            user_input = {"gender": gender, "hemoglobin": hemoglobin}
        except Exception as e:
            prediction_text = f"<span style='color:red;'>Error: {str(e)}</span>"
    return render_template("dashboard.html", prediction_text=prediction_text, user_input=user_input)

if __name__ == "__main__":
    app.run(debug=True)