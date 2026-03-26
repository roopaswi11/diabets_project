from flask import Flask, render_template, request
import os
import matplotlib.pyplot as plt

from model.diabetes_model import (
    analyze_diabetes,
    doctor_alert,
    diet_recommendation,
    meal_plan
)

from utils.ocr_reader import (
    extract_text_from_image,
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_sugar_values
)

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

sugar_history = []


# ---------------------------
# HOME PAGE
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------------------
# REPORT UPLOAD + ANALYSIS
# ---------------------------
@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["report"]

    if file.filename == "":
        return "No file selected"

    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    filename = file.filename.lower()

    # Detect file type
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(path)

    elif filename.endswith(".docx"):
        text = extract_text_from_docx(path)

    else:
        text = extract_text_from_image(path)

    # Extract sugar values
    fasting, pp, hba1c = extract_sugar_values(text)

    # Diabetes analysis
    status = analyze_diabetes(fasting, pp, hba1c)

    alert = doctor_alert(status)

    diet = diet_recommendation(status)

    # Generate meal plan
    plan = meal_plan(status)

    # Store fasting value for dashboard graph
    if fasting:
        sugar_history.append(float(fasting))

    return render_template(
        "dashboard.html",
        fasting=fasting,
        pp=pp,
        hba1c=hba1c,
        status=status,
        alert=alert,
        diet=diet,
        meal=plan,
        raw_text=text
    )


# ---------------------------
# SUGAR HISTORY GRAPH
# ---------------------------
@app.route("/dashboard")
def dashboard():

    plt.figure()

    if len(sugar_history) > 0:
        plt.plot(sugar_history)

    plt.xlabel("Record")
    plt.ylabel("Fasting Sugar")
    plt.title("Sugar Tracking")

    graph_path = "static/graph.png"

    plt.savefig(graph_path)

    plt.close()

    return render_template("dashboard.html", graph=graph_path)


# ---------------------------
# CHATBOT
# ---------------------------
@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():

    answer = ""

    if request.method == "POST":

        question = request.form["question"].lower()

        if "rice" in question:
            answer = "Brown rice in moderate quantity is recommended for diabetics."

        elif "fruit" in question:
            answer = "Low glycemic fruits like apples, berries, and guava are recommended."

        elif "exercise" in question:
            answer = "Walking 30 minutes daily helps control blood sugar."

        elif "diet" in question:
            answer = "A diabetic diet should include whole grains, vegetables, lean protein and less sugar."

        else:
            answer = "Please consult a doctor for detailed medical advice."

    return render_template("chatbot.html", answer=answer)


# ---------------------------
# RUN SERVER
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)