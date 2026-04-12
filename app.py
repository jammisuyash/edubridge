"""
app.py — EduBridge Flask Backend
Gemini AI integrated. Works on Vercel and locally.
"""

import os
import json
import urllib.request
import urllib.error

# ── Only load .env file when running LOCALLY ──────────────────
# On Vercel: env vars are already injected before Python starts.
# We must NOT call load_dotenv() on Vercel because it can
# accidentally overwrite injected vars with .env.example values.
# Solution: only load dotenv if NOT on Vercel.
if not os.environ.get("VERCEL"):
    try:
        from dotenv import load_dotenv
        load_dotenv(override=False)
    except ImportError:
        pass  # dotenv not installed — fine, we read os.environ directly

from flask import Flask, render_template, request, jsonify, session

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
app.secret_key = os.environ.get("SECRET_KEY", "edubridge-fallback-secret-2024")

# Vercel's filesystem: only /tmp is writable
# Vercel automatically sets the VERCEL environment variable
if os.environ.get("VERCEL"):
    ProgressTracker.DATA_DIR = "/tmp/edubridge_data"
else:
    ProgressTracker.DATA_DIR = os.environ.get("DATA_DIR", "data")

doubt_solver = DoubtSolver()
quiz_engine  = QuizEngine()


# ─────────────────────────────────────────────
# GEMINI HELPER
# ─────────────────────────────────────────────

def call_gemini(question: str) -> str:
    """
    Calls Google Gemini 2.0 Flash API using urllib (Python built-in).
    Free tier — no credit card needed.
    Get key at: https://aistudio.google.com/apikey
    """
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    if not api_key:
        raise ValueError("NO_KEY")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={api_key}"
    )

    body = json.dumps({
        "systemInstruction": {
            "parts": [{
                "text": (
                    "You are EduBridge, a friendly study companion for Indian students "
                    "aged 14-22. Structure your answer as: "
                    "1) Brief explanation (2-3 sentences) "
                    "2) A simple example "
                    "3) One quick memory tip. "
                    "Keep the total response under 200 words. Use simple English."
                )
            }]
        },
        "contents": [{"parts": [{"text": question}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 500
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]

    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8")
        if e.code == 400:
            raise ValueError(f"BAD_REQUEST: {body_text[:200]}")
        if e.code == 403:
            raise ValueError("INVALID_KEY")
        if e.code == 429:
            raise ValueError("RATE_LIMIT")
        raise ValueError(f"HTTP_{e.code}: {body_text[:200]}")

    except urllib.error.URLError as e:
        raise ConnectionError(f"NETWORK_ERROR: {str(e)}")


def get_tracker():
    return ProgressTracker(session.get("student_id", "guest"))


# ─────────────────────────────────────────────
# PAGE
# ─────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


# ─────────────────────────────────────────────
# DEBUG — shows exactly what the server sees
# Visit /api/debug in browser to diagnose issues
# ─────────────────────────────────────────────

@app.route("/api/debug")
def debug():
    key = os.environ.get("GEMINI_API_KEY", "")
    secret = os.environ.get("SECRET_KEY", "")

    # Mask the key safely
    if key and len(key) > 8:
        masked = key[:6] + "..." + key[-4:]
    elif key:
        masked = "too_short_" + str(len(key)) + "_chars"
    else:
        masked = "NOT_SET"

    return jsonify({
        "status": "ok",
        "GEMINI_API_KEY": masked,
        "key_length": len(key),
        "key_starts_AIza": key.startswith("AIza"),
        "key_is_placeholder": key in ("", "your-AIza-key-here", "paste-your-key-here"),
        "gemini_configured": len(key) > 10 and key.startswith("AIza"),
        "SECRET_KEY_set": len(secret) > 5,
        "VERCEL": os.environ.get("VERCEL", "not_set"),
        "FLASK_ENV": os.environ.get("FLASK_ENV", "not_set"),
        "data_dir": ProgressTracker.DATA_DIR,
        "python_version": __import__("sys").version,
    })


# ─────────────────────────────────────────────
# API: STUDENT
# ─────────────────────────────────────────────

@app.route("/api/set-student", methods=["POST"])
def set_student():
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
# API: SOLVE DOUBT  — local KB first, then Gemini
# ─────────────────────────────────────────────

@app.route("/api/solve", methods=["POST"])
def solve_doubt():
    try:
        data = request.get_json()
        if not data:
            raise InvalidInputError("No data received.")
        question = data.get("question", "").strip()
        if not question:
            raise InvalidInputError("Question cannot be empty.")

        # Layer 1 — local knowledge base (instant, offline)
        try:
            result = doubt_solver.solve(question)
            get_tracker().log_doubt(question, result.get("title", ""))
            result["source"] = "local"
            return jsonify({"success": True, "result": result, "source": "local"})
        except TopicNotFoundError:
            pass

        # Layer 2 — Gemini AI
        try:
            ai_text = call_gemini(question)
            get_tracker().log_doubt(question, "AI")
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

        except ValueError as ve:
            err = str(ve)
            # Return a helpful message based on the error code
            if "NO_KEY" in err:
                msg = "Gemini API key not set. Add GEMINI_API_KEY in Vercel environment variables."
            elif "INVALID_KEY" in err:
                msg = "Gemini API key is invalid. Check the key in your Vercel settings."
            elif "RATE_LIMIT" in err:
                msg = "Gemini rate limit hit. Wait 1 minute and try again."
            else:
                msg = f"Gemini error: {err}"

            return jsonify({
                "success": True,
                "source":  "error",
                "result": {
                    "title":     "Could Not Get AI Answer",
                    "steps":     [msg, "Visit /api/debug to diagnose the issue."],
                    "example":   "",
                    "tip":       "",
                    "topic_key": "error",
                }
            })

        except ConnectionError as ce:
            return jsonify({
                "success": True,
                "source":  "error",
                "result": {
                    "title":     "Network Error",
                    "steps":     [str(ce)],
                    "example":   "",
                    "tip":       "This usually means the Vercel function cannot reach the internet.",
                    "topic_key": "error",
                }
            })

    except InvalidInputError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except EduBridgeError as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ─────────────────────────────────────────────
# API: QUIZ
# ─────────────────────────────────────────────

@app.route("/api/quiz/start", methods=["POST"])
def start_quiz():
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
    cards = []
    for i, card_tuple in enumerate(FLASHCARDS):
        tag, question, answer, example = card_tuple
        cards.append({"id": i, "tag": tag, "question": question,
                      "answer": answer, "example": example})
    return jsonify({"success": True, "flashcards": cards, "total": len(cards)})


# ─────────────────────────────────────────────
# API: PROGRESS
# ─────────────────────────────────────────────

@app.route("/api/progress", methods=["GET"])
def get_progress():
    try:
        return jsonify({"success": True, "report": get_tracker().get_full_report()})
    except EduBridgeError as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/progress/clear", methods=["POST"])
def clear_progress():
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
# API: TOPICS + AI STATUS
# ─────────────────────────────────────────────

@app.route("/api/topics", methods=["GET"])
def get_topics():
    return jsonify({"success": True, "topics": doubt_solver.get_all_topics()})


@app.route("/api/quiz/topics", methods=["GET"])
def get_quiz_topics():
    return jsonify({"success": True, "topics": quiz_engine.get_all_topics()})


@app.route("/api/ai/status", methods=["GET"])
def ai_status():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    ok  = bool(key and len(key) > 10 and key.startswith("AIza"))
    return jsonify({
        "success":    True,
        "configured": ok,
        "model":      "gemini-2.0-flash (free)" if ok else "not configured",
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
# LOCAL RUN ONLY (Vercel uses api/index.py)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    key = os.environ.get("GEMINI_API_KEY", "")
    ai  = "✅ Gemini ready" if (key and key.startswith("AIza")) else "⚠️  Set GEMINI_API_KEY in .env"
    print(f"\n{'='*45}\n  EduBridge — http://localhost:5000\n  {ai}\n{'='*45}\n")
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
