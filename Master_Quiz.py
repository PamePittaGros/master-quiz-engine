import json
import random
import datetime
from pathlib import Path

# -------------------------
# 📁 BASE DIRECTORY
# -------------------------

BASE_DIR = Path(__file__).parent

# -------------------------
# 🧠 NORMALIZE ANSWERS
# -------------------------

def normalize(text):
    text = text.lower().strip()

    word_to_number = {
        "zero": "0", "one": "1", "two": "2", "three": "3",
        "four": "4", "five": "5", "six": "6", "seven": "7"
    }

    synonyms = {
        "boolean": "bool",
        "integer": "int"
    }

    text = word_to_number.get(text, text)
    text = synonyms.get(text, text)

    return text

# -------------------------
# 📦 LOAD QUESTIONS
# -------------------------

def load_questions(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON error in {file_path}: {e}")
        return []

# -------------------------
# 📁 GET TOPIC PATH
# -------------------------

def get_topic_path(topic):
    return BASE_DIR / topic / "questions.json"

# -------------------------
# 🎯 FILTER QUESTIONS
# -------------------------

def filter_questions(questions, difficulty):
    if difficulty == "all":
        return questions
    return [q for q in questions if q.get("difficulty", "").lower() == difficulty]

# -------------------------
# 🎲 SELECT QUESTIONS
# -------------------------

def select_questions(questions, amount):
    return random.sample(questions, min(amount, len(questions)))

# -------------------------
# 🎮 NORMAL QUIZ
# -------------------------

def run_quiz(questions):
    score = 0
    streak = 0
    wrong = []
    weak_topics = {}

    i = 0
    while i < len(questions):
        q = questions[i]

        print(f"\n📘 Q{i+1}/{len(questions)}: {q['question']}")
        user = normalize(input("Your answer: "))

        answers = [normalize(a) for a in q.get("answer", [])]

        if user in answers:
            print("✅ Correct")
            score += 1
            streak += 1
            print(f"🔥 Streak: {streak}")
        else:
            print(f"❌ Wrong (Accepted: {', '.join(q.get('answer', []))})")

            print("💡 Type the correct answer to continue:")
            while True:
                retry_input = normalize(input("> "))
                if retry_input in answers:
                    break
                print("❌ Try again.")

            streak = 0
            wrong.append(q)

            topic = q.get("topic", "unknown")
            weak_topics[topic] = weak_topics.get(topic, 0) + 1

            questions.append(q)

        i += 1

    return score, wrong, weak_topics

# -------------------------
# 🎯 MULTIPLE CHOICE QUIZ
# -------------------------

def run_mcq(questions):
    if len(questions) < 2:
        print("⚠️ Not enough questions. Switching to normal.")
        return run_quiz(questions)

    score = 0
    streak = 0
    wrong = []
    weak_topics = {}

    for i, q in enumerate(questions, 1):
        correct = normalize(q["answer"][0])

        pool = set()
        for item in questions:
            if item != q:
                for ans in item.get("answer", []):
                    pool.add(normalize(ans))

        pool.discard(correct)
        distractors = random.sample(list(pool), min(3, len(pool)))

        options = [correct] + distractors
        random.shuffle(options)

        print(f"\n📘 Q{i}/{len(questions)}: {q['question']}")
        for idx, opt in enumerate(options, 1):
            print(f"{idx}. {opt}")

        try:
            choice = int(input("Choose: "))
            if not 1 <= choice <= len(options):
                raise ValueError
            user_answer = options[choice - 1]
        except (ValueError, IndexError):
            print("❌ Invalid input")
            wrong.append(q)
            streak = 0
            continue

        if normalize(user_answer) == correct:
            print("✅ Correct")
            score += 1
            streak += 1
            print(f"🔥 Streak: {streak}")
        else:
            print(f"❌ Wrong (Correct: {correct})")

            print("💡 Type the correct answer:")
            while True:
                retry_input = normalize(input("> "))
                if retry_input == correct:
                    break
                print("❌ Try again.")

            streak = 0
            wrong.append(q)

            topic = q.get("topic", "unknown")
            weak_topics[topic] = weak_topics.get(topic, 0) + 1

    return score, wrong, weak_topics

# -------------------------
# 📄 SAVE REPORT
# -------------------------

def save_report(score, total, wrong, topic, difficulty, mode, weak_topics):
    folder = BASE_DIR / "reports" / topic / difficulty
    folder.mkdir(parents=True, exist_ok=True)

    percentage = (score / total) * 100 if total else 0
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = folder / f"{mode}_{timestamp}.txt"

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(f"Score: {score}/{total}\n")
        f.write(f"Accuracy: {percentage:.2f}%\n\n")

        if wrong:
            f.write("Wrong Answers:\n")
            for w in wrong:
                f.write(f"- {w['question']} → {', '.join(w.get('answer', []))}\n")

        if weak_topics:
            f.write("\nWeak Topics:\n")
            for t, c in sorted(weak_topics.items(), key=lambda x: -x[1]):
                f.write(f"{t}: {c}\n")

    print(f"📄 Saved: {file_name}")

# -------------------------
# 🚀 MAIN
# -------------------------

def main():
    print("🎮 MASTER QUIZ ENGINE\n")

    # ✅ SORTED TOPICS (NEW)
    topics = sorted(
        [d.name for d in BASE_DIR.iterdir()
         if d.is_dir() and (d / "questions.json").exists()]
    )

    print("Available topics:")
    for t in topics:
        print("-", t)

    topic_map = {t.lower(): t for t in topics}

    while True:
        topic_input = input("\nChoose topic: ").strip().lower()
        if topic_input in topic_map:
            topic = topic_map[topic_input]
            break
        print("❌ Invalid topic.")

    difficulty = input("Difficulty (easy / medium / hard / all): ").strip().lower()

    allowed_sizes = [10, 25, 50, 100]
    while True:
        try:
            size = int(input("Test size (10 / 25 / 50 / 100): "))
            if size in allowed_sizes:
                break
            print("❌ Choose 10, 25, 50, or 100.")
        except ValueError:
            print("❌ Enter a number.")

    mode_input = input("Mode (1 = normal / 2 = MCQ): ")
    mode, run_func = ("mcq", run_mcq) if mode_input == "2" else ("normal", run_quiz)

    path = get_topic_path(topic)
    questions = load_questions(path)

    if not questions:
        print("❌ No questions found.")
        return

    filtered = filter_questions(questions, difficulty)
    test = select_questions(filtered, size)

    if not test:
        print("❌ No matching questions.")
        return

    score, wrong, weak_topics = run_func(test)

    total = len(test)
    percentage = (score / total) * 100

    print(f"\n🏆 Score: {score}/{total}")
    print(f"✅ Accuracy: {percentage:.1f}%")

    save_report(score, total, wrong, topic, difficulty, mode, weak_topics)


if __name__ == "__main__":
    main()