"""
modules/doubt_solver.py
Matches student questions to topics using string functions and dictionaries.

Syllabus concepts demonstrated:
  - Strings & string methods : lower(), strip(), split()
  - Dictionaries             : TOPIC_BANK lookup
  - Functions                : modular, single-responsibility
  - Loops                    : scanning keywords
  - Sets                     : unique word matching
"""

from modules.knowledge_base import TOPIC_BANK
from modules.exceptions import TopicNotFoundError, InvalidInputError


class DoubtSolver:
    """
    Finds the best matching topic for a student's question.
    Uses string-matching logic to score each topic in the knowledge base.
    """

    def solve(self, question: str) -> dict:
        """
        Takes a student question and returns the best matching topic.

        Args:
            question (str): The raw text of the student's doubt.

        Returns:
            dict: The matched topic data including title, steps, example, tip.

        Raises:
            InvalidInputError : If the question is empty or too short.
            TopicNotFoundError: If no matching topic is found.
        """
        # ── Input validation (Exception handling concept)
        if not question or not question.strip():
            raise InvalidInputError("Question cannot be empty.")
        if len(question.strip()) < 3:
            raise InvalidInputError("Question is too short. Please be more specific.")

        # ── Normalize: String methods (lower, strip, split)
        normalized = question.lower().strip()
        query_words = set(normalized.split())   # Set for fast membership checks

        best_topic_key = None
        best_score = 0

        # ── Loop through all topics in the dictionary
        for topic_key, topic_data in TOPIC_BANK.items():
            score = 0
            keywords = topic_data["keywords"]   # list of keyword strings

            for keyword in keywords:
                # Skip single-char keywords — they cause false matches
                if len(keyword) <= 2:
                    continue

                # Full keyword phrase found in question (highest score)
                if keyword in normalized:
                    score += len(keyword.split()) * 4

                # Partial: every word of a multi-word keyword must match
                kw_words = [w for w in keyword.split() if len(w) > 3]
                if kw_words and all(w in query_words for w in kw_words):
                    score += len(kw_words) * 2

            if score > best_score:
                best_score = score
                best_topic_key = topic_key

        # Minimum score of 4 required — prevents false matches on common words
        if best_topic_key is None or best_score < 4:
            raise TopicNotFoundError(
                f"No topic found for: '{question}'. "
                "Try asking about recursion, for loops, dictionaries, lists, sets, "
                "functions, strings, exceptions, file I/O, modules, photosynthesis, or Newton's laws."
            )

        # ── Return a copy of the matched topic (dictionary access)
        result = dict(TOPIC_BANK[best_topic_key])
        result["topic_key"] = best_topic_key
        return result

    def get_all_topics(self) -> list:
        """Returns list of all available topic titles."""
        # List comprehension — Syllabus: Lists + Loops
        return [data["title"] for data in TOPIC_BANK.values()]
