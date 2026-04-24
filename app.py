from flask import Flask, render_template, request
import json
import random

app = Flask(__name__)

# Load questions
with open("questions.json", "r") as file:
    questions = json.load(file)

# Home page
@app.route("/", methods=["GET", "POST"])
def index():
    question = random.choice(questions)

    if request.method == "POST":
        user_answer = request.form["answer"].lower()
        correct_answers = [a.lower() for a in question["answers"]]

        if user_answer in correct_answers:
            result = "Correct!"
        else:
            result = "Wrong!"

        return render_template("result.html", result=result)

    return render_template("index.html", question=question["question"])


if __name__ == "__main__":
    app.run(debug=True)