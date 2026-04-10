"""
modules/quiz_engine.py
Generates and evaluates quizzes from the knowledge base.

Syllabus concepts demonstrated:
  - Lists         : question banks stored as lists of dicts
  - Sets          : tracking weak areas (unique topic strings)
  - Functions     : generate_quiz, evaluate, shuffle
  - Modules       : importing random for shuffle
  - Dictionaries  : question format, feedback structure
  - Loops         : iterating questions and answers
"""

import random
from modules.knowledge_base import QUIZ_BANK
from modules.exceptions import InvalidInputError, TopicNotFoundError, QuizError


class QuizEngine:
    """
    Handles quiz generation and answer evaluation.
    Uses lists of dicts for questions and sets for weak area tracking.
    """

    def get_all_topics(self) -> list:
        """Returns a list of all available quiz topics."""
        return list(QUIZ_BANK.keys())   # dict.keys() → list

    def generate_quiz(self, topic: str, count: int = 5) -> list:
        """
        Returns a shuffled list of quiz questions for the given topic.

        Args:
            topic (str): The topic name (e.g. "Python", "Science").
            count (int): Number of questions to return.

        Returns:
            list: A list of question dictionaries (without the answer).

        Raises:
            InvalidInputError : If topic is empty or count is invalid.
            TopicNotFoundError: If topic doesn't exist in QUIZ_BANK.
        """
        if not topic or not topic.strip():
            raise InvalidInputError("Topic name cannot be empty.")
        if count < 1 or count > 20:
            raise InvalidInputError("Question count must be between 1 and 20.")

        topic = topic.strip()
        if topic not in QUIZ_BANK:
            raise TopicNotFoundError(
                f"Topic '{topic}' not found. "
                f"Available topics: {', '.join(QUIZ_BANK.keys())}"
            )

        # Get all questions for this topic
        all_questions = list(QUIZ_BANK[topic])   # make a copy with list()

        # Shuffle using random module (Modules concept)
        random.shuffle(all_questions)

        # Take only the requested number (list slicing concept)
        selected = all_questions[:min(count, len(all_questions))]

        # Return questions WITHOUT the answer (don't cheat!)
        sanitized = []
        for i, q in enumerate(selected):
            sanitized.append({
                "id": i,
                "q": q["q"],
                "options": q["options"],
                # answer and explanation NOT sent to frontend
            })

        return sanitized

    def evaluate(self, questions: list, answers: list) -> tuple:
        """
        Scores a submitted quiz and identifies weak areas.

        Args:
            questions (list): Original questions list with answers.
            answers   (list): Student's submitted answers (list of ints).

        Returns:
            tuple: (score, feedback_list, weak_areas_set)

        Syllabus: Tuples (return), Sets (weak_areas), Loops, Lists
        """
        if not questions or not answers:
            raise QuizError("Questions and answers cannot be empty.")
        if len(questions) != len(answers):
            raise QuizError("Number of answers doesn't match number of questions.")

        score = 0
        feedback = []          # list of dicts
        weak_areas = set()     # set — automatically unique

        # Loop through each question-answer pair
        for i, (question, student_answer) in enumerate(zip(questions, answers)):
            correct_answer = question.get("answer")
            is_correct = (student_answer == correct_answer)

            if is_correct:
                score += 1
            else:
                # Track weak area using set (unique values only)
                weak_areas.add(question["q"][:40])

            feedback.append({
                "question_id": i,
                "correct": is_correct,
                "selected": student_answer,
                "correct_answer": correct_answer,
                "explanation": question.get("explanation", ""),
            })

        # Return as tuple (Tuples concept)
        return score, feedback, list(weak_areas)

    def get_questions_with_answers(self, topic: str) -> list:
        """Returns full question data including answers — used for evaluation."""
        if topic not in QUIZ_BANK:
            raise TopicNotFoundError(f"Topic '{topic}' not found.")
        return list(QUIZ_BANK[topic])
