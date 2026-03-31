"""
Data structures for representing programming exercises from Exercism tracks.
"""

import json

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class Difficulty(Enum):
    """Exercise difficulty levels."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ExerciseStatus(Enum):
    """Exercise status in the track."""

    LOCKED = "locked"
    AVAILABLE = "available"
    COMPLETED = "completed"


@dataclass
class TestCase:
    """Represents a test case for an exercise."""

    input_data: Any
    expected_output: Any
    description: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "input": self.input_data,
            "expected": self.expected_output,
            "description": self.description,
        }


@dataclass
class Exercise:
    """Represents a programming exercise from Exercism."""

    # Core identifiers
    slug: str
    language: str
    track: str

    # Exercise metadata
    title: str
    description: str
    difficulty: Difficulty
    status: ExerciseStatus = ExerciseStatus.AVAILABLE

    # Exercise content
    starter_code: Optional[str] = None
    solution_code: Optional[str] = None
    test_cases: List[TestCase] = None

    # Additional metadata
    topics: List[str] = None
    prerequisites: List[str] = None
    uuid: Optional[str] = None

    def __post_init__(self):
        if self.test_cases is None:
            self.test_cases = []
        if self.topics is None:
            self.topics = []
        if self.prerequisites is None:
            self.prerequisites = []

    def to_dict(self) -> Dict:
        """Convert exercise to dictionary representation."""
        return {
            "slug": self.slug,
            "language": self.language,
            "track": self.track,
            "title": self.title,
            "description": self.description,
            "difficulty": self.difficulty.value,
            "status": self.status.value,
            "starter_code": self.starter_code,
            "solution_code": self.solution_code,
            "test_cases": [tc.to_dict() for tc in self.test_cases],
            "topics": self.topics,
            "prerequisites": self.prerequisites,
            "uuid": self.uuid,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Exercise":
        """Create exercise from dictionary representation."""
        test_cases = []
        for tc in data.get("test_cases", []):
            test_cases.append(
                TestCase(
                    input_data=tc["input"],
                    expected_output=tc["expected"],
                    description=tc.get("description"),
                )
            )

        return cls(
            slug=data["slug"],
            language=data["language"],
            track=data["track"],
            title=data["title"],
            description=data["description"],
            difficulty=Difficulty(data["difficulty"]),
            status=ExerciseStatus(data.get("status", "available")),
            starter_code=data.get("starter_code"),
            solution_code=data.get("solution_code"),
            test_cases=test_cases,
            topics=data.get("topics", []),
            prerequisites=data.get("prerequisites", []),
            uuid=data.get("uuid"),
        )

    def to_json(self) -> str:
        """Convert exercise to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "Exercise":
        """Create exercise from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)


@dataclass
class ExerciseTrack:
    """Represents an Exercism language track."""

    language: str
    track_id: str
    exercises: List[Exercise]

    # Track metadata
    description: Optional[str] = None
    active: bool = True

    def __post_init__(self):
        if not self.exercises:
            self.exercises = []

    def add_exercise(self, exercise: Exercise):
        """Add an exercise to the track."""
        self.exercises.append(exercise)

    def get_exercise_by_slug(self, slug: str) -> Optional[Exercise]:
        """Get exercise by slug."""
        for exercise in self.exercises:
            if exercise.slug == slug:
                return exercise
        return None

    def get_exercises_by_difficulty(self, difficulty: Difficulty) -> List[Exercise]:
        """Get exercises filtered by difficulty."""
        return [ex for ex in self.exercises if ex.difficulty == difficulty]

    def to_dict(self) -> Dict:
        """Convert track to dictionary representation."""
        return {
            "language": self.language,
            "track_id": self.track_id,
            "description": self.description,
            "active": self.active,
            "exercises": [ex.to_dict() for ex in self.exercises],
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "ExerciseTrack":
        """Create track from dictionary representation."""
        exercises = [Exercise.from_dict(ex) for ex in data.get("exercises", [])]

        return cls(
            language=data["language"],
            track_id=data["track_id"],
            exercises=exercises,
            description=data.get("description"),
            active=data.get("active", True),
        )
