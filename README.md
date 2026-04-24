📚 Adaptive Quiz Engine (Python)
Overview

A modular quiz engine built in Python that reinforces learning through active recall, feedback, and targeted practice.

Originally developed as a terminal-based quiz, this project evolved into a more structured system focused on learning effectiveness and scalability.

🚀 Key Features

Topic-based question system using JSON datasets

Difficulty filtering (easy / medium / hard / all)

Randomized, non-repeating question selection

Support for multiple correct answers

Input normalization (e.g., "4" vs "four")

Performance tracking with saved session reports

Organized result storage by topic and difficulty

Cross-platform (Windows, Mac, Linux)

🧠 Learning-Focused Design

This project emphasizes:

Active recall over passive review

Immediate feedback for reinforcement

Identifying weak areas through incorrect answers

🛠 Tech Stack

Python

JSON (question storage)

File I/O (result tracking)

CLI (command-line interface)

📁 Project Structure
master-quiz-engine/
│
├── Master_Quiz.py          # Main quiz engine
├── Python/                 # Python questions
│     └── questions.json
├── Java/                   # Java questions
│     └── questions.json
├── HTML/                   # HTML questions
│     └── questions.json
└── Master test results/    # Saved quiz results
⚙️ How It Works

User selects a topic

User selects difficulty

User selects number of questions

Questions are randomly selected (no repeats)

Answers are validated against accepted formats

Score is calculated

Results are saved to a file

▶️ Getting Started
1. Install Python (3.10+ recommended)
2. Navigate to project folder
3. Run the program
python Master_Quiz.py
📦 Question Format (JSON)
{
  "question": "What is 2 + 2?",
  "answer": ["4", "four"],
  "difficulty": "easy"
}
📊 Example Output
Q1: What is 2 + 2?
> 4
✅ Correct

Q2: What is Python?
> snake
❌ Incorrect
📄 Results

After each session, results are saved automatically:

Master test results/
   ├── Python/
   │     ├── easy/
   │     │     └── result_YYYY-MM-DD.txt

Each report includes:

Score

Incorrect answers

Timestamp

🔭 Future Improvements

Web-based interface (Flask or FastAPI)

Progress visualization (charts, analytics)

Adaptive difficulty system

User profiles and persistent tracking

💼 What This Project Demonstrates

Writing modular, maintainable Python code

Structuring scalable projects across multiple datasets

Handling edge cases and input validation

Designing systems with user learning in mind

👨‍💻 Author

Taylor
Aspiring Software Engineer focused on building practical, real-world systems
