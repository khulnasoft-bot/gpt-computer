"""
Exercise loader for importing and managing Exercism exercises.
"""

import json
import os

from pathlib import Path
from typing import Dict, List, Optional

import yaml

from exercise import Difficulty, Exercise, ExerciseStatus, ExerciseTrack, TestCase


class ExerciseLoader:
    """Loads and manages exercises from various sources."""

    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent
        self.tracks: Dict[str, ExerciseTrack] = {}

    def load_track_from_directory(self, language: str, track_dir: str) -> ExerciseTrack:
        """Load a track from a directory structure."""
        track_path = Path(track_dir)

        # Load track metadata
        metadata_file = track_path / "track_metadata.json"
        metadata = {}
        if metadata_file.exists():
            with open(metadata_file, "r") as f:
                metadata = json.load(f)

        # Create track
        track = ExerciseTrack(
            language=language,
            track_id=metadata.get("track_id", language),
            exercises=[],  # Initialize with empty list
            description=metadata.get("description"),
            active=metadata.get("active", True),
        )

        # Load exercises
        exercises_dir = track_path / "exercises"
        if exercises_dir.exists():
            for exercise_dir in exercises_dir.iterdir():
                if exercise_dir.is_dir():
                    exercise = self._load_exercise_from_directory(
                        exercise_dir, language, track.track_id
                    )
                    if exercise:
                        track.add_exercise(exercise)

        return track

    def _load_exercise_from_directory(
        self, exercise_dir: Path, language: str, track_id: str
    ) -> Optional[Exercise]:
        """Load a single exercise from its directory."""
        # Load exercise metadata
        metadata_file = exercise_dir / "metadata.json"
        if not metadata_file.exists():
            return None

        with open(metadata_file, "r") as f:
            metadata = json.load(f)

        # Load starter code
        starter_code = None
        starter_file = (
            exercise_dir / "starter.py"
            if language == "python"
            else exercise_dir / f"starter.{self._get_file_extension(language)}"
        )
        if starter_file.exists():
            with open(starter_file, "r") as f:
                starter_code = f.read()

        # Load solution code
        solution_code = None
        solution_file = (
            exercise_dir / "solution.py"
            if language == "python"
            else exercise_dir / f"solution.{self._get_file_extension(language)}"
        )
        if solution_file.exists():
            with open(solution_file, "r") as f:
                solution_code = f.read()

        # Load test cases
        test_cases = []
        test_file = exercise_dir / "test_cases.json"
        if test_file.exists():
            with open(test_file, "r") as f:
                test_data = json.load(f)
                for tc in test_data:
                    test_cases.append(
                        TestCase(
                            input_data=tc["input"],
                            expected_output=tc["expected"],
                            description=tc.get("description"),
                        )
                    )

        # Create exercise
        exercise = Exercise(
            slug=metadata["slug"],
            language=language,
            track=track_id,
            title=metadata["title"],
            description=metadata["description"],
            difficulty=Difficulty(metadata.get("difficulty", "medium")),
            status=ExerciseStatus(metadata.get("status", "available")),
            starter_code=starter_code,
            solution_code=solution_code,
            test_cases=test_cases,
            topics=metadata.get("topics", []),
            prerequisites=metadata.get("prerequisites", []),
            uuid=metadata.get("uuid"),
        )

        return exercise

    def _get_file_extension(self, language: str) -> str:
        """Get file extension for a programming language."""
        extensions = {
            "python": "py",
            "javascript": "js",
            "java": "java",
            "cpp": "cpp",
            "c": "c",
            "rust": "rs",
            "go": "go",
            "ruby": "rb",
            "csharp": "cs",
            "php": "php",
        }
        return extensions.get(language, "txt")

    def load_exercise_from_file(self, file_path: str) -> Exercise:
        """Load a single exercise from a JSON file."""
        with open(file_path, "r") as f:
            data = json.load(f)
        return Exercise.from_dict(data)

    def save_exercise_to_file(self, exercise: Exercise, file_path: str):
        """Save an exercise to a JSON file."""
        with open(file_path, "w") as f:
            json.dump(exercise.to_dict(), f, indent=2)

    def load_all_tracks(self) -> Dict[str, ExerciseTrack]:
        """Load all tracks from the base directory."""
        self.tracks = {}

        for lang_dir in self.base_path.iterdir():
            if lang_dir.is_dir() and lang_dir.name not in ["__pycache__", ".git"]:
                language = lang_dir.name
                try:
                    track = self.load_track_from_directory(language, lang_dir)
                    self.tracks[language] = track
                except Exception as e:
                    print(f"Error loading track {language}: {e}")

        return self.tracks

    def get_track(self, language: str) -> Optional[ExerciseTrack]:
        """Get a specific track by language."""
        return self.tracks.get(language)

    def get_all_exercises(self) -> List[Exercise]:
        """Get all exercises from all tracks."""
        exercises = []
        for track in self.tracks.values():
            exercises.extend(track.exercises)
        return exercises

    def get_exercises_by_language(self, language: str) -> List[Exercise]:
        """Get exercises for a specific language."""
        track = self.get_track(language)
        return track.exercises if track else []

    def get_exercises_by_difficulty(self, difficulty: Difficulty) -> List[Exercise]:
        """Get all exercises of a specific difficulty."""
        exercises = []
        for track in self.tracks.values():
            exercises.extend(track.get_exercises_by_difficulty(difficulty))
        return exercises


class ExercismImporter:
    """Imports exercises from Exercism format."""

    @staticmethod
    def import_exercise_from_config(
        config_path: str, starter_path: str, solution_path: str, test_path: str
    ) -> Exercise:
        """Import an exercise from Exercism configuration files."""

        # Load configuration
        with open(config_path, "r") as f:
            if config_path.endswith(".yml") or config_path.endswith(".yaml"):
                config = yaml.safe_load(f)
            else:
                config = json.load(f)

        # Extract metadata from config
        exercise_slug = config.get("exercise", "").lower().replace(" ", "-")
        language = config.get("language", "unknown")

        # Load starter code
        starter_code = None
        if starter_path and os.path.exists(starter_path):
            with open(starter_path, "r") as f:
                starter_code = f.read()

        # Load solution code
        solution_code = None
        if solution_path and os.path.exists(solution_path):
            with open(solution_path, "r") as f:
                solution_code = f.read()

        # Parse test cases from test file
        test_cases = ExercismImporter._parse_test_cases(test_path, language)

        # Create exercise
        exercise = Exercise(
            slug=exercise_slug,
            language=language,
            track=language,  # Use language as track for now
            title=config.get("exercise", exercise_slug.replace("-", " ").title()),
            description=config.get("blurb", ""),
            difficulty=Difficulty.MEDIUM,  # Default difficulty
            starter_code=starter_code,
            solution_code=solution_code,
            test_cases=test_cases,
            topics=config.get("topics", []),
            uuid=config.get("uuid"),
        )

        return exercise

    @staticmethod
    def _parse_test_cases(test_path: str, language: str) -> List[TestCase]:
        """Parse test cases from test file (basic implementation)."""
        test_cases = []

        if not os.path.exists(test_path):
            return test_cases

        # This is a simplified implementation
        # In a real implementation, you'd parse the actual test file
        # based on the testing framework used for each language

        if language == "python":
            # Parse pytest/unittest style tests
            with open(test_path, "r") as f:
                f.read()
                # Simple regex-based parsing for demonstration
                # In practice, you'd use AST parsing

        return test_cases
