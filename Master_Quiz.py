import json
import random
import datetime
from pathlib import Path


# -------------------------
# 📁 BASE DIRECTORY
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

def filter_questions(questions, difficulty, language):
    filtered = questions

    if difficulty != "all":
        filtered = [q for q in filtered if q.get("difficulty", "").lower() == difficulty]

    if language != "all":
        filtered = [q for q in filtered if q.get("language", "python").lower() == language]

    return filtered


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

    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}: {q['question']}")
        user = input("Your answer: ").strip()

        answers = [a.lower().strip() for a in q.get("answer", [])]
        user_clean = user.lower()

        if user_clean in answers:
            print("✅ Correct\n")
            score += 1
            streak += 1
            print(f"🔥 Streak: {streak}\n")
        else:
            print(f"❌ Wrong (Accepted answers: {', '.join(q.get('answer', []))})\n")
            streak = 0
            wrong.append(q)
            topic = q.get("topic", "unknown")
            weak_topics[topic] = weak_topics.get(topic, 0) + 1

    return score, wrong, weak_topics


# -------------------------
# 🎯 MULTIPLE CHOICE QUIZ (FIXED)
# -------------------------

def run_mcq(questions):
    if len(questions) < 2:
        print("⚠️ Not enough questions to generate MCQs (need ≥2). Falling back to normal quiz.")
        return run_quiz(questions)

    score = 0
    streak = 0
    wrong = []
    weak_topics = {}

    for i, q in enumerate(questions, 1):
        correct = q["answer"][0]
        # Create *unique* distractors: use other questions’ first answers (excluding duplicates)
        all_other_answers = set()
        for item in questions:
            if item != q:
                for ans in item.get("answer", []):
                    ans_clean = ans.strip().lower()
                    all_other_answers.add(ans_clean)

        # Remove the correct answer itself
        all_other_answers.discard(correct.lower())

        # Pick up to 3 unique wrong answers (ensure ≥1 distractor)
        distractors = random.sample(list(all_other_answers), min(3, max(0, len(all_other_answers))))
        options = [correct] + [a.strip() for a in distractors]

        if len(options) < 2:
            print("⚠️ Not enough unique answer options. Skipping this question.")
            continue

        random.shuffle(options)

        print(f"\nQ{i}: {q['question']}")
        for idx, opt in enumerate(options, 1):
            print(f"{idx}. {opt}")

        try:
            choice = int(input("\nChoose (1–{}): ".format(len(options))).strip())
            if not 1 ≤ choice ≤ len(options):
                raise ValueError("Out of range")
            user_answer = options[choice - 1]
        except (ValueError, IndexError):
            print("❌ Invalid input. Skipping question.\n")
            streak = 0
            wrong.append(q)
            continue

        if user_answer.lower() == correct.lower():
            print("✅ Correct\n")
            score += 1
            streak += 1
            print(f"🔥 Streak: {streak}\n")
        else:
            print(f"❌ Wrong (Correct: {correct})\n")
            streak = 0
            wrong.append(q)
            topic = q.get("topic", "unknown")
            weak_topics[topic] = weak_topics.get(topic, 0) + 1

    return score, wrong, weak_topics


# -------------------------
# 📄 SAVE REPORT (FIXED DUPLICATE)
# -------------------------

def save_report(score, total, wrong, topic, difficulty, mode, weak_topics):
    desktop = Path.home() / "Desktop"
    folder = desktop / "Master test results" / topic / difficulty
    folder.mkdir(parents=True, exist_ok=True)

    percentage = (score / total) * 100 if total > 0 else 0

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = folder / f"{mode}_result_{timestamp}.txt"

    with open(file_name, "w", encoding="utf-8") as f:
        f.write("QUIZ REPORT\n")
        f.write("=" * 40 + "\n")
        f.write(f"Mode: {mode}\n")
        f.write(f"Topic: {topic}\n")
        f.write(f"Difficulty: {difficulty}\n")
        f.write(f"Score: {score}/{total}\n")
        f.write(f"Percentage: {percentage:.2f}%\n\n")

        if wrong:
            f.write("WRONG ANSWERS:\n")
            for w in wrong:
                f.write("-" * 40 + "\n")
                f.write(f"Q: {w['question']}\n")
                f.write(f"Correct answer(s): {', '.join(w.get('answer', []))}\n")
                f.write(f"Topic: {w.get('topic', 'N/A')}\n\n")

        if weak_topics:
            f.write("WEAK TOPICS:\n")
            for t, c in sorted(weak_topics.items(), key=lambda x: -x[1]):
                f.write(f"- {t}: {c} mistake(s)\n")

    print(f"📄 Report saved: {file_name}")
    return file_name


# -------------------------
# 🚀 MAIN MENU
# -------------------------

def main():
    print("🎮 MASTER QUIZ ENGINE\n")
    print("Available topics:")
    dirs = [d.name for d in BASE_DIR.iterdir() if d.is_dir()]
    for d in sorted(dirs):
        print(f"- {d}")

    topic = input("\nChoose topic: ").strip().lower()
    difficulty = input("Difficulty (easy / medium / hard / all): ").strip().lower()
    language = input("Language (python / java / all): ").strip().lower()
    size = int(input("Test size (e.g., 10/25/50): "))
    mode_input = input("Mode (1 = normal / 2 = MCQ): ")

    # Validate & map mode
    if mode_input == "2":
        mode, run_func = "mcq", run_mcq
    else:
        mode, run_func = "normal", run_quiz

    path = get_topic_path(topic)
    questions = load_questions(path)

    if not questions:
        print("❌ No questions loaded. Exiting.")
        return

    filtered = filter_questions(questions, difficulty, language)
    test = select_questions(filtered, min(size, len(filtered)))

    if not test:
        print("❌ No questions matched your filters.")
        return

    score, wrong, weak_topics = run_func(test)

    # Final output
    total = len(test)
    print("\n🏆 FINAL SCORE:", f"{score}/{total}")
    percentage = (score / total) * 100
    print(f"✅ Accuracy: {percentage:.1f}%")

    if weak_topics:
        print("\n🔍 Weak areas (by mistakes):")
        for t, c in sorted(weak_topics.items(), key=lambda x: -x[1]):
            print(f" - {t}: {c}")

    # Save report
    save_report(score, total, wrong, topic, difficulty, mode, weak_topics)


if __name__ == "__main__":
    main()
