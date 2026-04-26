from flask import Flask, render_template, request, redirect, url_for, session
import json
import random
from pathlib import Path

app = Flask(__name__)
app.secret_key = "dev-key"

BASE_DIR = Path(__file__).parent


# -------------------------
# LOAD QUESTIONS
# -------------------------
def load_questions(topic):
    path = BASE_DIR / topic / "questions.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


# -------------------------
# HOME (TOPICS ONLY)
# -------------------------
@app.route("/")
def home():
    topics = [
        d.name for d in BASE_DIR.iterdir()
        if d.is_dir() and (d / "questions.json").exists()
    ]
    return render_template("topics.html", topics=topics)


# -------------------------
# SELECT NUMBER PAGE
# -------------------------
@app.route("/select/<topic>")
def select(topic):
    return render_template("select.html", topic=topic)


# -------------------------
# QUIZ PAGE
# -------------------------
@app.route("/quiz/<topic>")
def quiz(topic):

    num = int(request.args.get("num", 10))

    all_q = load_questions(topic)

    session["questions"] = random.sample(all_q, min(num, len(all_q)))
    session["index"] = 0
    session["score"] = 0
    session["topic"] = topic

    return redirect(url_for("question"))


# -------------------------
# QUESTION LOOP
# -------------------------
@app.route("/question", methods=["GET", "POST"])
def question():

    questions = session.get("questions", [])
    index = session.get("index", 0)

    if index >= len(questions):
        return redirect(url_for("result"))

    q = questions[index]

    feedback = ""

    if request.method == "POST":
        user = request.form.get("answer", "").lower()
        correct = [a.lower() for a in q["answer"]]

        if user in correct:
            session["score"] += 1
            feedback = "✅ Correct"
        else:
            feedback = f"❌ Wrong (Answer: {q['answer'][0]})"

        session["index"] += 1
        return redirect(url_for("question"))

    return render_template("question.html", question=q, feedback=feedback, index=index+1)


# -------------------------
# RESULT
# -------------------------
@app.route("/result")
def result():
    score = session.get("score", 0)
    total = len(session.get("questions", []))
    session.clear()
    return render_template("result.html", score=score, total=total)


if __name__ == "__main__":
    app.run(debug=True)