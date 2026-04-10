"""
app.py — EduBridge Flask Backend
=================================
Free AI powered by Google Gemini (no credit card needed).

HOW TO RUN LOCALLY:
    1. Copy .env.example to .env and fill in your values
    2. pip install -r requirements.txt
    3. python app.py  →  open http://localhost:5000

HOW TO RUN ON VERCEL:
    Set these in Vercel Dashboard → Project → Settings → Environment Variables:
      SECRET_KEY   = any long random string
      GEMINI_API_KEY = your key from aistudio.google.com/apikey

SYLLABUS CONCEPTS:
    Functions, Dictionaries, Lists, Tuples, Sets,
    File I/O, Exception handling, Modules, Strings
"""

import os
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session

# Load .env file when running locally
# On Vercel, env vars are injected directly — load_dotenv() safely does nothing
load_dotenv()

from modules.doubt_solver     import DoubtSolver
from modules.quiz_engine      import QuizEngine
from modules.progress_tracker import ProgressTracker
from modules.knowledge_base   import FLASHCARDS
from modules.exceptions import (
    EduBridgeError, TopicNotFoundError, InvalidInputError, QuizError,
)


# ─────────────────────────────────────────────
# APP SETUP
# ─────────────────────────────────────────────

app = Flask(__name__)

# SECRET_KEY signs session cookies — must be set in Vercel env vars
app.secret_key = os.environ.get("SECRET_KEY", "change-this-in-production")

# On Vercel only /tmp is writable. Auto-detect via the VERCEL env var
# that Vercel injects automatically into every deployment.
if os.environ.get("VERCEL"):
    ProgressTracker.DATA_DIR = "/tmp/edubridge_data"
else:
    ProgressTracker.DATA_DIR = os.environ.get("DATA_DIR", "data")

doubt_solver = DoubtSolver()
quiz_engine  = QuizEngine()


# ─────────────────────────────────────────────
# GEMINI AI HELPER
# ─────────────────────────────────────────────

def call_gemini(question: str) -> str:
    """
    Call Google Gemini API using urllib (Python built-in — no extra library).
    Free tier: 1,500 requests/day. No credit card needed.
    Key from: https://aistudio.google.com/apikey

    Syllabus: Modules (urllib, json), Strings, Dictionaries, Exception handling
    """
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    if not api_key:
        raise ValueError("GEMINI_API_KEY not set.")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={api_key}"
    )

    # Build request payload as a dictionary, then JSON-encode it
    payload = json.dumps({
        "systemInstruction": {
            "parts": [{
                "text": (
                    "You are EduBridge, a friendly study companion for Indian students "
                    "aged 14-22. Answer clearly. Structure: 1) Brief explanation "
                    "2) Simple example 3) One quick tip. Max 150 words. Simple language."
                )
            }]
        },
        "contents": [{"parts": [{"text": question}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 400}
    }).encode("utf-8")

    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        if e.code == 403:
            raise ValueError("Invalid Gemini API key.")
        if e.code == 429:
            raise ValueError("Rate limit hit — wait 1 minute.")
        raise ValueError(f"Gemini error {e.code}: {body[:150]}")

    except urllib.error.URLError:
        raise ConnectionError("Cannot reach Gemini. Check internet connection.")


def get_tracker():
    """Get ProgressTracker for the current session's student."""
    return ProgressTracker(session.get("student_id", "guest"))


# ─────────────────────────────────────────────
# PAGE ROUTE
# ─────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


# ─────────────────────────────────────────────
# API: STUDENT SESSION
# ─────────────────────────────────────────────

@app.route("/api/set-student", methods=["POST"])
def set_student():
    """Save student name to session. Syllabus: Strings, Exception handling"""
    try:
        data = request.get_json()
        if not data:
            raise InvalidInputError("No data received.")
        name = data.get("name", "").strip()
        if not name or len(name) < 2:
            raise InvalidInputError("Name must be at least 2 characters.")
        session["student_id"] = name.lower().replace(" ", "_")
        return jsonify({"success": True, "student_id": session["student_id"]})
    except InvalidInputError as e:
        return jsonify({"success": False, "error": str(e)}), 400


# ─────────────────────────────────────────────
# API: DOUBT SOLVER  (local KB + Gemini fallback)
# ─────────────────────────────────────────────

@app.route("/api/solve", methods=["POST"])
def solve_doubt():
    """
    Layer 1: Local string-matching on TOPIC_BANK (instant, offline)
    Layer 2: Gemini AI for anything outside the local knowledge base
    Syllabus: Strings, Dictionaries, Functions, Exception handling
    """
    try:
        data = request.get_json()
        if not data:
            raise InvalidInputError("No data received.")
        question = data.get("question", "").strip()
        if not question:
            raise InvalidInputError("Question cannot be empty.")

        # ── Layer 1: local knowledge base
        try:
            result = doubt_solver.solve(question)
            get_tracker().log_doubt(question, result.get("title", ""))
            result["source"] = "local"
            return jsonify({"success": True, "result": result, "source": "local"})
        except TopicNotFoundError:
            pass  # fall through to Gemini

        # ── Layer 2: Gemini AI
        try:
            ai_text = call_gemini(question)
            get_tracker().log_doubt(question, "AI Answer")
            return jsonify({
                "success": True,
                "source":  "ai",
                "result": {
                    "title":     "AI Answer",
                    "steps":     [ai_text],
                    "example":   "",
                    "tip":       "Answered by Google Gemini AI (free tier).",
                    "topic_key": "ai",
                }
            })

        except ValueError as e:
            # Key not configured — give friendly setup message
            return jsonify({
                "success": True,
                "source":  "no_key",
                "result": {
                    "title": "Topic Not in Local KB",
                    "steps": [
                        f"'{question}' isn't in my local knowledge base.",
                        "To answer any question, set GEMINI_API_KEY in your Vercel environment variables.",
                        "Get a free key (no credit card) at: aistudio.google.com/apikey",
                    ],
                    "example": "",
                    "tip": "Free Gemini tier: 1,500 requests/day with just a Google account.",
                    "topic_key": "no_key",
                }
            })

        except ConnectionError as e:
            return jsonify({"success": False, "error": str(e)}), 503

    except InvalidInputError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except EduBridgeError as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ─────────────────────────────────────────────
# API: QUIZ
# ─────────────────────────────────────────────

@app.route("/api/quiz/start", methods=["POST"])
def start_quiz():
    """Generate quiz questions. Answers stored in session — not sent to browser."""
    try:
        data = request.get_json()
        if not data:
            raise InvalidInputError("No data received.")
        topic = data.get("topic", "").strip()
        count = int(data.get("count", 6))
        questions_display = quiz_engine.generate_quiz(topic, count)
        full_questions     = quiz_engine.get_questions_with_answers(topic)
        session["quiz_topic"]     = topic
        session["quiz_questions"] = full_questions[:count]
        return jsonify({
            "success":   True,
            "topic":     topic,
            "questions": questions_display,
            "count":     len(questions_display),
        })
    except InvalidInputError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except TopicNotFoundError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@app.route("/api/quiz/submit", methods=["POST"])
def submit_quiz():
    """Score answers, save to file. Syllabus: Tuples, Lists, Sets, File I/O"""
    try:
        data = request.get_json()
        if not data:
            raise InvalidInputError("No data received.")
        answers   = data.get("answers", [])
        topic     = session.get("quiz_topic", "Unknown")
        questions = session.get("quiz_questions", [])
        if not questions:
            raise QuizError("No active quiz. Please start a new quiz.")
        if not answers:
            raise InvalidInputError("No answers submitted.")
        score, feedback, weak_areas = quiz_engine.evaluate(questions, answers)
        percentage = round((score / len(questions)) * 100)
        get_tracker().log_quiz(topic, score, len(questions), weak_areas)
        return jsonify({
            "success":    True,
            "score":      score,
            "total":      len(questions),
            "percentage": percentage,
            "feedback":   feedback,
            "weak_areas": weak_areas,
            "topic":      topic,
        })
    except (InvalidInputError, QuizError) as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except EduBridgeError as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ─────────────────────────────────────────────
# API: FLASHCARDS
# ─────────────────────────────────────────────

@app.route("/api/flashcards", methods=["GET"])
def get_flashcards():
    """Return flashcards from list of tuples. Syllabus: Tuples, Lists, Loops"""
    cards = []
    for i, card_tuple in enumerate(FLASHCARDS):
        tag, question, answer, example = card_tuple  # tuple unpacking
        cards.append({"id": i, "tag": tag, "question": question,
                      "answer": answer, "example": example})
    return jsonify({"success": True, "flashcards": cards, "total": len(cards)})


# ─────────────────────────────────────────────
# API: PROGRESS
# ─────────────────────────────────────────────

@app.route("/api/progress", methods=["GET"])
def get_progress():
    """Read student progress JSON file. Syllabus: File I/O, Dictionaries"""
    try:
        return jsonify({"success": True, "report": get_tracker().get_full_report()})
    except EduBridgeError as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/progress/clear", methods=["POST"])
def clear_progress():
    """Delete student progress file. Syllabus: File I/O, os module"""
    try:
        filepath = os.path.join(
            ProgressTracker.DATA_DIR,
            f"{session.get('student_id', 'guest')}.json"
        )
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"success": True, "message": "Progress cleared."})
    except OSError as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ─────────────────────────────────────────────
# API: TOPIC LISTS
# ─────────────────────────────────────────────

@app.route("/api/topics", methods=["GET"])
def get_topics():
    return jsonify({"success": True, "topics": doubt_solver.get_all_topics()})


@app.route("/api/quiz/topics", methods=["GET"])
def get_quiz_topics():
    return jsonify({"success": True, "topics": quiz_engine.get_all_topics()})


# ─────────────────────────────────────────────
# API: AI STATUS CHECK
# ─────────────────────────────────────────────

@app.route("/api/ai/status", methods=["GET"])
def ai_status():
    """Check if Gemini API key is configured."""
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    ok  = bool(key and len(key) > 10)
    return jsonify({
        "success":    True,
        "configured": ok,
        "model":      "gemini-2.0-flash (free)" if ok else "not configured",
        "setup_url":  "https://aistudio.google.com/apikey",
    })


# ─────────────────────────────────────────────
# ERROR HANDLERS
# ─────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "error": "Not found."}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"success": False, "error": "Server error."}), 500


# ─────────────────────────────────────────────
# START (local only — Vercel uses api/index.py)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    key = os.environ.get("GEMINI_API_KEY", "")
    ai  = "✅ Gemini AI ready" if (key and len(key) > 10) else "⚠️  No GEMINI_API_KEY set"
    print(f"\n{'='*48}\n  EduBridge — http://localhost:5000\n  {ai}\n{'='*48}\n")
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
