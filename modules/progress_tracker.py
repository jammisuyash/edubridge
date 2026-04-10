"""
modules/progress_tracker.py
Saves and loads student progress using file I/O and dictionaries.

Syllabus concepts demonstrated:
  - File I/O      : open, read, write, with statement, json
  - Dictionaries  : progress data stored as nested dicts
  - Lists         : session history as list of records
  - Sets          : weak topics as unique strings
  - Functions     : single-responsibility design
  - Exceptions    : try/except/finally for file safety
  - Modules       : json, os, datetime
"""

import json
import os
from datetime import datetime
from modules.exceptions import FileStorageError


class ProgressTracker:
    """
    Tracks and persists student progress using file-based storage.
    Each student gets their own JSON file in the data/ directory.
    """

    DATA_DIR = "data"   # folder where student files are saved

    def __init__(self, student_id: str):
        """
        Initialise tracker for a specific student.

        Args:
            student_id (str): Unique identifier for the student.
        """
        self.student_id = student_id
        self.filepath = os.path.join(self.DATA_DIR, f"{student_id}.json")
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Create the data directory if it doesn't exist."""
        if not os.path.exists(self.DATA_DIR):
            os.makedirs(self.DATA_DIR)

    def _load(self) -> dict:
        """
        Load student progress from file.
        Returns an empty progress dict if file doesn't exist.

        Syllabus: File I/O (open, read), Exception handling, JSON module
        """
        try:
            with open(self.filepath, "r") as f:       # File open for reading
                return json.load(f)                    # Modules: json.load
        except FileNotFoundError:
            # First time — return a clean empty progress dictionary
            return self._empty_progress()
        except json.JSONDecodeError:
            raise FileStorageError("Progress file is corrupted. Starting fresh.")

    def _save(self, data: dict):
        """
        Save student progress to file.

        Syllabus: File I/O (open, write), JSON module
        """
        try:
            with open(self.filepath, "w") as f:        # File open for writing
                json.dump(data, f, indent=2)            # Modules: json.dump
        except OSError as e:
            raise FileStorageError(f"Could not save progress: {e}")

    def _empty_progress(self) -> dict:
        """Returns a fresh empty progress dictionary."""
        return {
            "student_id": self.student_id,
            "total_sessions": 0,
            "total_doubts": 0,
            "total_quizzes": 0,
            "total_score": 0,
            "streak_days": 0,
            "last_study_date": "",
            "weak_topics": [],      # list of weak topic strings
            "quiz_history": [],     # list of quiz result dicts
            "doubt_history": [],    # list of asked questions
        }

    def _update_streak(self, data: dict) -> dict:
        """Update the daily study streak based on today's date."""
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = ""

        if data["last_study_date"]:
            # Calculate yesterday's date for streak checking
            from datetime import timedelta
            last = datetime.strptime(data["last_study_date"], "%Y-%m-%d")
            yesterday = (last + timedelta(days=1)).strftime("%Y-%m-%d")

        if data["last_study_date"] == today:
            pass  # Same day — streak unchanged
        elif today == yesterday:
            data["streak_days"] += 1   # Consecutive day
        else:
            data["streak_days"] = 1    # Reset streak

        data["last_study_date"] = today
        return data

    def log_doubt(self, question: str, topic: str):
        """
        Record a doubt that was asked by the student.

        Syllabus: File I/O, Dictionaries, Lists (append)
        """
        data = self._load()
        data["total_doubts"] += 1
        data["total_sessions"] += 1
        data = self._update_streak(data)

        # Append to doubt history (list.append — Lists concept)
        data["doubt_history"].append({
            "question": question,
            "topic": topic,
            "time": datetime.now().strftime("%H:%M"),
            "date": datetime.now().strftime("%Y-%m-%d"),
        })

        # Keep only last 50 doubts (list slicing — Lists concept)
        data["doubt_history"] = data["doubt_history"][-50:]

        self._save(data)

    def log_quiz(self, topic: str, score: int, total: int, weak_areas: list):
        """
        Record a completed quiz result.

        Syllabus: File I/O, Dictionaries, Lists, Sets (for weak topics)
        """
        data = self._load()
        data["total_quizzes"] += 1
        data["total_sessions"] += 1
        data["total_score"] += score
        data = self._update_streak(data)

        # Add quiz to history
        data["quiz_history"].append({
            "topic": topic,
            "score": score,
            "total": total,
            "percentage": round((score / total) * 100) if total > 0 else 0,
            "time": datetime.now().strftime("%H:%M"),
            "date": datetime.now().strftime("%Y-%m-%d"),
        })
        data["quiz_history"] = data["quiz_history"][-30:]  # keep last 30

        # Merge weak areas using set (unique values — Sets concept)
        existing_weak = set(data["weak_topics"])
        existing_weak.update(weak_areas)
        data["weak_topics"] = list(existing_weak)[-20:]    # keep last 20

        self._save(data)

    def get_summary(self) -> dict:
        """Returns a summary dict for display on the dashboard."""
        data = self._load()
        total_q  = data["total_quizzes"]
        total_sc = data["total_score"]
        avg = round(total_sc / total_q) if total_q > 0 else 0

        return {
            "student_id":     data["student_id"],
            "total_sessions": data["total_sessions"],
            "total_doubts":   data["total_doubts"],
            "total_quizzes":  total_q,
            "avg_score":      avg,
            "streak_days":    data["streak_days"],
            "weak_topics":    data["weak_topics"],
        }

    def get_full_report(self) -> dict:
        """Returns the full progress report including history."""
        data = self._load()
        summary = self.get_summary()

        # Recent quiz scores for chart — last 10 results
        recent_scores = [
            {"topic": q["topic"], "score": q["percentage"], "date": q["date"]}
            for q in data["quiz_history"][-10:]     # list slicing
        ]

        summary["recent_scores"] = recent_scores
        summary["quiz_history"]  = list(reversed(data["quiz_history"][-8:]))
        return summary
