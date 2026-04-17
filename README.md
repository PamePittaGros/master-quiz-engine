📘 Master Quiz Engine

A simple, portable quiz system built with Python.
It loads questions from JSON files and runs interactive quizzes in the terminal.

🚀 Features
Multiple topics (Python, Java, HTML, etc.)
Difficulty system (easy / medium / hard / all)
Random question selection
No repeated questions in one test
Supports multiple answers per question
Saves test results to a text file
Works on Windows, Mac, Linux (portable)
📁 Project Structure
master-quiz-engine/
│
├── Master_Quiz.py
├── Python/
│     └── questions.json
│
├── Java/
│     └── questions.json
│
├── HTML/
│     └── questions.json
│
└── Master test results/
🧠 How it works
User selects a topic
User selects difficulty
User selects number of questions (25 / 50 / 100)
Quiz runs in terminal
Score is calculated
Results are saved to a .txt file
▶️ How to run
Step 1

Install Python (3.10+ recommended)

Step 2

Open terminal in project folder

Step 3

Run:

python Master_Quiz.py
📦 Question Format (JSON)

Each question looks like this:

{
  "question": "What is 2 + 2?",
  "answer": ["4", "four"],
  "difficulty": "easy"
}
🧪 Example Output
Q1: What is 2 + 2?
> 4
✅ Correct

Q2: What is Python?
> snake
❌ Wrong
📄 Results

After each quiz, a report is saved automatically:

Master test results/
   ├── Python/
   │     ├── easy/
   │     │     └── result_2026-04-16.txt

Includes:

score
wrong answers
timestamp
🎯 Goals of this project

This project is built to:

Practice Python fundamentals
Learn file handling (JSON, TXT)
Build a scalable quiz system
Prepare for real software engineering projects
🔧 Future Improvements
GUI version (Tkinter or Web)
Leaderboard system
Timer per question
Database storage
User accounts
👨‍💻 Author

Built by Taylor
Learning software engineering step by step.
