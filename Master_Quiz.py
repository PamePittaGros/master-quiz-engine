import json
import random
import datetime
from pathlib import Path

# -------------------------
# 📁 BASE DIRECTORY (PORTABLE)
# -------------------------

BASE_DIR = Path(__file__).parent

# -------------------------
# 📦 LOAD QUESTIONS
# -------------------------

def load_questions(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print("❌ File not found:", file_path)
        return []

# -------------------------
# 📁 GET TOPIC PATH (AUTO)
# -------------------------

def get_topic_path(topic):
    return BASE_DIR / topic / "questions.json"

# -------------------------
# 🎯 FILTER DIFFICULTY
# -------------------------

def filter_questions(questions, difficulty):
    if difficulty == "all":
        return questions

    return [q for q in questions if q["difficulty"] == difficulty]

# -------------------------
# 🎲 SELECT QUESTIONS
# -------------------------

def select_questions(questions, amount):
    return random.sample(questions, min(amount, len(questions)))

# -------------------------
# 🎮 QUIZ ENGINE
# -------------------------

def run_quiz(questions):
    score = 0
    wrong = []

    for i, q in enumerate(questions, 1):
        user = input(f"Q{i}: {q['question']} ? ")

        answers = [a.lower().strip() for a in q["answer"]]

        if user.lower().strip() in answers:
            print("✅ Correct\n")
            score += 1
        else:
            print(f"❌ Wrong (Correct: {q['answer'][0]})\n")
            wrong.append(q)

    return score, wrong

# -------------------------
# 📄 SAVE REPORT (CROSS-PLATFORM)
# -------------------------

def save_report(score, total, wrong, topic, difficulty):
    desktop = Path.home() / "Desktop"
    folder = desktop / "Master test results" / topic / difficulty
    folder.mkdir(parents=True, exist_ok=True)

    file_name = folder / f"result_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(file_name, "w", encoding="utf-8") as file:
        file.write("QUIZ REPORT\n")
        file.write("=================\n")
        file.write(f"Topic: {topic}\n")
        file.write(f"Difficulty: {difficulty}\n")
        file.write(f"Score: {score}/{total}\n\n")
        file.write("WRONG ANSWERS:\n")

        for w in wrong:
            file.write("\n-----------------\n")
            file.write(f"Q: {w['question']}\n")
            file.write(f"Correct: {w['answer']}\n")

    print(f"📄 Saved: {file_name}")

# -------------------------
# 🚀 MAIN MENU
# -------------------------

print("🎮 PORTABLE QUIZ ENGINE")

print("\nAvailable topics:")
for folder in BASE_DIR.iterdir():
    if folder.is_dir():
        print("-", folder.name)

topic = input("\nChoose topic: ").lower()

difficulty = input("Difficulty (easy / medium / hard / all): ").lower()

size = int(input("Test size (25 / 50 / 100): "))

# -------------------------
# 📁 LOAD DATA (PORTABLE)
# -------------------------

path = get_topic_path(topic)
questions = load_questions(path)

# -------------------------
# 🎯 PROCESS
# -------------------------

questions = filter_questions(questions, difficulty)
test = select_questions(questions, size)

score, wrong = run_quiz(test)

print("\n🏆 FINAL SCORE:", score, "/", len(test))

save_report(score, len(test), wrong, topic, difficulty)