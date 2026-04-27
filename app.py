from flask import Flask, render_template, request, redirect, url_for, session
import json
import random
from pathlib import Path

app = Flask(__name__)
app.secret_key = "safe-key-change-me"

BASE_DIR = Path(__file__).parent


# -------------------------
# LOAD QUESTIONS SAFELY
# -------------------------
def load_questions(topic):
    path = BASE_DIR / topic / "questions.json"

    if not path.exists():
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


# -------------------------
# HOME PAGE
# -------------------------
@app.route("/")
def home():
    topics = [
        d.name for d in BASE_DIR.iterdir()
        if d.is_dir() and (d / "questions.json").exists()
    ]

    return render_template("topics.html", topics=topics)


# -------------------------
# SELECT TOPIC
# -------------------------
@app.route("/select/<topic>")
def select(topic):
    if not (BASE_DIR / topic / "questions.json").exists():
        return redirect(url_for("home"))

    return render_template("select.html", topic=topic)


# -------------------------
# START QUIZ
# -------------------------
@app.route("/quiz/<topic>")
def quiz(topic):

    questions = load_questions(topic)

    if not questions:
        return redirect(url_for("home"))

    try:
        num = int(request.args.get("num", 10))
    except:
        num = 10

    num = max(1, min(num, 100))

    session["questions"] = random.sample(questions, min(num, len(questions)))
    session["index"] = 0
    session["score"] = 0
    session["topic"] = topic

    return redirect(url_for("question"))


# -------------------------
# QUESTION ENGINE
# -------------------------
@app.route("/question", methods=["GET", "POST"])
def question():

    questions = session.get("questions", [])
    index = session.get("index", 0)

    if not questions:
        return redirect(url_for("home"))

    if index >= len(questions):
        return redirect(url_for("result"))

    q = questions[index]
    total = len(questions)

    feedback = session.pop("feedback", "")

    if request.method == "POST":

        user = request.form.get("answer", "").lower()
        correct = [a.lower() for a in q.get("answer", [])]

        if user in correct:
            session["score"] = session.get("score", 0) + 1
            session["feedback"] = "✅ Correct"
        else:
            session["feedback"] = f"❌ Wrong (Answer: {q['answer'][0]})"

        session["index"] = index + 1

        return redirect(url_for("question"))

    return render_template(
        "question.html",
        question=q,
        index=index + 1,
        total=total,
        feedback=feedback
    )


# -------------------------
# RESULT PAGE
# -------------------------
@app.route("/result")
def result():

    score = session.get("score", 0)
    questions = session.get("questions", [])
    total = len(questions)

    session.clear()

    return render_template("result.html", score=score, total=total)


# -------------------------
# 404 SAFETY
# -------------------------
@app.errorhandler(404)
def not_found(e):
    return redirect(url_for("home"))


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)