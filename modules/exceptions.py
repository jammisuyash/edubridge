"""
modules/exceptions.py
Custom exception classes for EduBridge.

Syllabus concept: User-defined Exceptions, Try/Except/Finally
"""


class EduBridgeError(Exception):
    """Base exception for all EduBridge errors."""
    pass


class TopicNotFoundError(EduBridgeError):
    """Raised when no matching topic is found for a student's question."""
    pass


class InvalidInputError(EduBridgeError):
    """Raised when user input is empty, too short, or invalid."""
    pass


class QuizError(EduBridgeError):
    """Raised when quiz data is missing or malformed."""
    pass


class FileStorageError(EduBridgeError):
    """Raised when reading or writing progress files fails."""
    pass
