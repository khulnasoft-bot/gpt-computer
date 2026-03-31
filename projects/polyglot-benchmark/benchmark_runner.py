"""
Benchmark runner for executing and evaluating exercises across multiple languages.
"""

import json
import os
import subprocess
import tempfile
import time

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from exercise import Exercise, ExerciseTrack, TestCase
from loader import ExerciseLoader


class ExecutionResult(Enum):
    """Result of executing an exercise."""

    SUCCESS = "success"
    FAILURE = "failure"
    ERROR = "error"
    TIMEOUT = "timeout"


@dataclass
class BenchmarkResult:
    """Result of benchmarking an exercise."""

    exercise: Exercise
    execution_result: ExecutionResult
    execution_time: float
    output: str
    error: Optional[str] = None
    test_results: List[bool] = None

    def __post_init__(self):
        if self.test_results is None:
            self.test_results = []

    def to_dict(self) -> Dict:
        return {
            "exercise_slug": self.exercise.slug,
            "language": self.exercise.language,
            "execution_result": self.execution_result.value,
            "execution_time": self.execution_time,
            "output": self.output,
            "error": self.error,
            "test_results": self.test_results,
            "tests_passed": sum(self.test_results),
            "total_tests": len(self.test_results),
            "success_rate": sum(self.test_results) / len(self.test_results)
            if self.test_results
            else 0.0,
        }


class LanguageExecutor:
    """Executes exercises for a specific programming language."""

    def __init__(self, language: str, timeout: int = 30):
        self.language = language
        self.timeout = timeout

    def execute_code(
        self, code: str, test_cases: List[TestCase]
    ) -> Tuple[ExecutionResult, str, float, List[bool]]:
        """Execute code with test cases and return results."""
        start_time = time.time()

        try:
            if self.language == "python":
                return self._execute_python(code, test_cases)
            elif self.language == "javascript":
                return self._execute_javascript(code, test_cases)
            elif self.language == "rust":
                return self._execute_rust(code, test_cases)
            else:
                return (
                    ExecutionResult.ERROR,
                    f"Unsupported language: {self.language}",
                    0.0,
                    [],
                )

        except subprocess.TimeoutExpired:
            return ExecutionResult.TIMEOUT, "Execution timeout", self.timeout, []
        except Exception as e:
            return ExecutionResult.ERROR, str(e), time.time() - start_time, []

    def _execute_python(
        self, code: str, test_cases: List[TestCase]
    ) -> Tuple[ExecutionResult, str, float, List[bool]]:
        """Execute Python code."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            f.write("\n\n# Test execution\n")
            f.write("import sys\n")
            f.write("import json\n")
            f.write("results = []\n")

            for i, test_case in enumerate(test_cases):
                if isinstance(test_case.input_data, list):
                    args = ", ".join(repr(arg) for arg in test_case.input_data)
                    f.write("try:\n")
                    f.write(f"    result = two_fer({args})\n")
                    f.write(
                        f"    results.append(result == {repr(test_case.expected_output)})\n"
                    )
                    f.write("except Exception as e:\n")
                    f.write("    results.append(False)\n")
                else:
                    f.write("try:\n")
                    f.write(f"    result = two_fer({repr(test_case.input_data)})\n")
                    f.write(
                        f"    results.append(result == {repr(test_case.expected_output)})\n"
                    )
                    f.write("except Exception as e:\n")
                    f.write("    results.append(False)\n")

            f.write("print(json.dumps(results))\n")
            temp_file = f.name

        try:
            start_time = time.time()
            result = subprocess.run(
                ["python3", temp_file],
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            execution_time = time.time() - start_time

            if result.returncode == 0:
                try:
                    test_results = json.loads(result.stdout.strip())
                    return (
                        ExecutionResult.SUCCESS,
                        result.stdout,
                        execution_time,
                        test_results,
                    )
                except json.JSONDecodeError:
                    return ExecutionResult.SUCCESS, result.stdout, execution_time, []
            else:
                return ExecutionResult.FAILURE, result.stderr, execution_time, []

        finally:
            os.unlink(temp_file)

    def _execute_javascript(
        self, code: str, test_cases: List[TestCase]
    ) -> Tuple[ExecutionResult, str, float, List[bool]]:
        """Execute JavaScript code using Node.js."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".mjs", delete=False
        ) as f:  # Use .mjs extension
            # Extract the function from the code
            f.write(code)
            f.write("\n\n// Test execution\n")
            f.write("const results = [];\n")

            for i, test_case in enumerate(test_cases):
                if isinstance(test_case.input_data, list):
                    args = ", ".join(json.dumps(arg) for arg in test_case.input_data)
                    f.write("try {\n")
                    f.write(f"    const result = isLeap({args});\n")
                    f.write(
                        f"    results.push(result === {json.dumps(test_case.expected_output)});\n"
                    )
                    f.write("} catch (e) {\n")
                    f.write("    results.push(false);\n")
                    f.write("}\n")
                else:
                    f.write("try {\n")
                    f.write(
                        f"    const result = isLeap({json.dumps(test_case.input_data)});\n"
                    )
                    f.write(
                        f"    results.push(result === {json.dumps(test_case.expected_output)});\n"
                    )
                    f.write("} catch (e) {\n")
                    f.write("    results.push(false);\n")
                    f.write("}\n")

            f.write("console.log(JSON.stringify(results));\n")
            temp_file = f.name

        try:
            start_time = time.time()
            result = subprocess.run(
                ["node", temp_file],
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            execution_time = time.time() - start_time

            if result.returncode == 0:
                try:
                    test_results = json.loads(result.stdout.strip())
                    return (
                        ExecutionResult.SUCCESS,
                        result.stdout,
                        execution_time,
                        test_results,
                    )
                except json.JSONDecodeError:
                    return ExecutionResult.SUCCESS, result.stdout, execution_time, []
            else:
                return ExecutionResult.FAILURE, result.stderr, execution_time, []

        finally:
            os.unlink(temp_file)

    def _execute_rust(
        self, code: str, test_cases: List[TestCase]
    ) -> Tuple[ExecutionResult, str, float, List[bool]]:
        """Execute Rust code."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create main.rs
            main_file = Path(temp_dir) / "main.rs"
            with open(main_file, "w") as f:
                f.write(code)
                f.write("\n\nfn main() {\n")
                f.write("    let mut results = Vec::new();\n")

                for i, test_case in enumerate(test_cases):
                    if (
                        isinstance(test_case.input_data, list)
                        and len(test_case.input_data) > 0
                    ):
                        # Parse datetime string for Rust
                        input_str = test_case.input_data[0]
                        f.write(
                            f'    let start_{i} = chrono::DateTime::parse_from_rfc3339("{input_str}").unwrap().with_timezone(&chrono::Utc);\n'
                        )
                        f.write(f"    let result_{i} = after(start_{i});\n")
                        f.write(
                            f'    let expected_{i} = chrono::DateTime::parse_from_rfc3339("{test_case.expected_output}").unwrap().with_timezone(&chrono::Utc);\n'
                        )
                        f.write(f"    results.push(result_{i} == expected_{i});\n")

                f.write(
                    '    println!("{{}}", serde_json::to_string(&results).unwrap());\n'
                )
                f.write("}\n")

            # Create Cargo.toml
            cargo_file = Path(temp_dir) / "Cargo.toml"
            with open(cargo_file, "w") as f:
                f.write(
                    """[package]
name = "temp_benchmark"
version = "0.1.0"
edition = "2021"

[dependencies]
chrono = "0.4"
serde_json = "1.0"
"""
                )

            try:
                start_time = time.time()
                # Build and run
                subprocess.run(
                    ["cargo", "build"],
                    cwd=temp_dir,
                    capture_output=True,
                    timeout=self.timeout,
                )
                result = subprocess.run(
                    ["cargo", "run"],
                    cwd=temp_dir,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                )
                execution_time = time.time() - start_time

                if result.returncode == 0:
                    try:
                        test_results = json.loads(result.stdout.strip())
                        return (
                            ExecutionResult.SUCCESS,
                            result.stdout,
                            execution_time,
                            test_results,
                        )
                    except json.JSONDecodeError:
                        return (
                            ExecutionResult.SUCCESS,
                            result.stdout,
                            execution_time,
                            [],
                        )
                else:
                    return ExecutionResult.FAILURE, result.stderr, execution_time, []

            except subprocess.TimeoutExpired:
                return ExecutionResult.TIMEOUT, "Execution timeout", self.timeout, []


class BenchmarkRunner:
    """Main benchmark runner for evaluating exercises."""

    def __init__(self, base_path: str = None):
        self.loader = ExerciseLoader(base_path)
        self.executors: Dict[str, LanguageExecutor] = {}
        self.results: List[BenchmarkResult] = []

    def load_exercises(self):
        """Load all exercises from the base directory."""
        return self.loader.load_all_tracks()

    def add_executor(self, language: str, executor: LanguageExecutor):
        """Add a language executor."""
        self.executors[language] = executor

    def run_exercise(
        self, exercise: Exercise, use_solution: bool = True
    ) -> BenchmarkResult:
        """Run a single exercise and return the benchmark result."""
        code = exercise.solution_code if use_solution else exercise.starter_code

        if not code:
            return BenchmarkResult(
                exercise=exercise,
                execution_result=ExecutionResult.ERROR,
                execution_time=0.0,
                output="",
                error="No code provided",
            )

        executor = self.executors.get(exercise.language)
        if not executor:
            return BenchmarkResult(
                exercise=exercise,
                execution_result=ExecutionResult.ERROR,
                execution_time=0.0,
                output="",
                error=f"No executor for language: {exercise.language}",
            )

        execution_result, output, execution_time, test_results = executor.execute_code(
            code, exercise.test_cases
        )

        return BenchmarkResult(
            exercise=exercise,
            execution_result=execution_result,
            execution_time=execution_time,
            output=output,
            test_results=test_results,
        )

    def run_track(
        self, track: ExerciseTrack, use_solution: bool = True
    ) -> List[BenchmarkResult]:
        """Run all exercises in a track."""
        results = []
        for exercise in track.exercises:
            result = self.run_exercise(exercise, use_solution)
            results.append(result)
            self.results.append(result)
        return results

    def run_all(self, use_solution: bool = True) -> List[BenchmarkResult]:
        """Run all exercises from all tracks."""
        self.load_exercises()
        all_results = []

        for track in self.loader.tracks.values():
            track_results = self.run_track(track, use_solution)
            all_results.extend(track_results)

        return all_results

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all benchmark results."""
        if not self.results:
            return {}

        total_exercises = len(self.results)
        successful = sum(
            1 for r in self.results if r.execution_result == ExecutionResult.SUCCESS
        )
        total_tests = sum(len(r.test_results) for r in self.results)
        passed_tests = sum(sum(r.test_results) for r in self.results)

        language_stats = {}
        for result in self.results:
            lang = result.exercise.language
            if lang not in language_stats:
                language_stats[lang] = {
                    "total": 0,
                    "successful": 0,
                    "avg_time": 0.0,
                    "total_tests": 0,
                    "passed_tests": 0,
                }

            language_stats[lang]["total"] += 1
            if result.execution_result == ExecutionResult.SUCCESS:
                language_stats[lang]["successful"] += 1
            language_stats[lang]["avg_time"] += result.execution_time
            language_stats[lang]["total_tests"] += len(result.test_results)
            language_stats[lang]["passed_tests"] += sum(result.test_results)

        # Calculate averages
        for stats in language_stats.values():
            stats["avg_time"] /= stats["total"]
            stats["success_rate"] = stats["successful"] / stats["total"]
            stats["test_success_rate"] = (
                stats["passed_tests"] / stats["total_tests"]
                if stats["total_tests"] > 0
                else 0
            )

        return {
            "total_exercises": total_exercises,
            "successful_exercises": successful,
            "overall_success_rate": successful / total_exercises,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "overall_test_success_rate": passed_tests / total_tests
            if total_tests > 0
            else 0,
            "language_stats": language_stats,
        }

    def save_results(self, filename: str):
        """Save benchmark results to a JSON file."""
        data = {
            "timestamp": time.time(),
            "summary": self.get_summary(),
            "results": [r.to_dict() for r in self.results],
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
