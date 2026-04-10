# EduBridge — Smart Study Companion

A full-stack PWA built with Python (Flask) + Google Gemini AI (free tier).
Doubt solver, adaptive quizzes, flashcards, and progress tracking — for every student.

---

## Project Structure

```
edubridge/
│
├── app.py                      ← Flask backend — all API routes
├── vercel.json                 ← Vercel deployment config
├── requirements.txt            ← Python dependencies (flask + python-dotenv)
├── .env.example                ← Template — copy to .env for local dev
├── .gitignore                  ← Excludes .env, data/, __pycache__
├── README.md
│
├── api/
│   └── index.py                ← Vercel serverless entry point
│
├── modules/                    ← Pure Python backend logic
│   ├── __init__.py
│   ├── knowledge_base.py       ← All topic data (dicts, lists, tuples)
│   ├── doubt_solver.py         ← String matching engine
│   ├── quiz_engine.py          ← Quiz generation + evaluation
│   ├── progress_tracker.py     ← File I/O for saving student progress
│   └── exceptions.py           ← Custom exception classes
│
├── templates/
│   └── index.html              ← Single-page HTML (served by Flask)
│
└── static/
    ├── css/style.css           ← All styles — glassmorphism + neomorphism
    ├── js/main.js              ← All JavaScript — UI, chat, quiz, flashcards
    ├── manifest.json           ← PWA manifest
    ├── sw.js                   ← Service worker for offline support
    └── icons/                  ← PWA icons
```

---

## Run Locally

```bash
# 1. Clone or unzip
cd edubridge

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Open .env and add your Gemini key

# 4. Run
python app.py

# 5. Open browser
# http://localhost:5000
```

### Environment variables (local `.env` file)

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | Any long random string. Generate: `python3 -c "import secrets; print(secrets.token_hex(32))"` |
| `GEMINI_API_KEY` | Yes | Free key from https://aistudio.google.com/apikey — no credit card |
| `FLASK_ENV` | No | `development` locally, `production` on Vercel |
| `PORT` | No | Defaults to `5000` |
| `DATA_DIR` | No | Defaults to `data/` — auto-set to `/tmp` on Vercel |

---

## Deploy to GitHub + Vercel

### Step 1 — Push to GitHub

```bash
# Inside the edubridge folder:
git init
git add .
git commit -m "Initial commit — EduBridge"

# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/edubridge.git
git branch -M main
git push -u origin main
```

> ✅ The `.env` file is in `.gitignore` — your API keys are never pushed to GitHub.

### Step 2 — Deploy on Vercel

1. Go to **https://vercel.com** → Sign up / Log in with GitHub
2. Click **"Add New Project"**
3. Click **"Import"** next to your `edubridge` repository
4. Vercel auto-detects `vercel.json` — no framework settings needed
5. Before clicking Deploy, click **"Environment Variables"** and add:

| Name | Value |
|---|---|
| `SECRET_KEY` | Your generated secret key |
| `GEMINI_API_KEY` | Your key from https://aistudio.google.com/apikey |
| `FLASK_ENV` | `production` |

6. Click **"Deploy"**
7. Vercel builds and gives you a live URL like `https://edubridge-abc123.vercel.app`

### Step 3 — Every future update

```bash
# Make your changes, then:
git add .
git commit -m "Your change description"
git push
# Vercel auto-deploys within 30 seconds
```

---

## API Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/` | Serves the main HTML page |
| POST | `/api/set-student` | Save student name to session |
| POST | `/api/solve` | Solve a doubt — local KB first, then Gemini AI |
| POST | `/api/quiz/start` | Start a quiz for a topic |
| POST | `/api/quiz/submit` | Submit answers, get score + feedback |
| GET | `/api/flashcards` | Get all 14 flashcards |
| GET | `/api/progress` | Get student's full progress report |
| POST | `/api/progress/clear` | Delete student's progress file |
| GET | `/api/topics` | List all doubt solver topics |
| GET | `/api/quiz/topics` | List all quiz subjects |
| GET | `/api/ai/status` | Check if Gemini AI is configured |

---

## Syllabus Concepts Map

| Python Concept | Where Used |
|---|---|
| Strings + String methods | `doubt_solver.py` — `lower()`, `strip()`, `split()` for question matching |
| Dictionaries | `knowledge_base.py` — entire topic bank stored as nested dicts |
| Lists | `quiz_engine.py` — question banks as lists, shuffle, slice |
| Tuples | `knowledge_base.py` — flashcards as `(tag, question, answer, example)` |
| Sets | `quiz_engine.py` — weak topics tracked in a set (unique values only) |
| Functions | Every module — single-responsibility functions throughout |
| Recursion | Quiz adaptive re-queuing concept |
| File I/O | `progress_tracker.py` — `open()`, `json.load()`, `json.dump()` |
| Exception handling | Every API route — `try/except/finally`, custom exception classes |
| Modules | `flask`, `os`, `json`, `random`, `datetime`, `urllib` |
| Branching / Loops | Throughout all modules |
