"""
GPT-Computer benchmark agent for the polyglot benchmark.
"""

import os
import tempfile

from typing import Optional

from benchmark_runner import BenchmarkRunner, LanguageExecutor
from exercise import Exercise

from gpt_computer.core.ai import AI
from gpt_computer.core.base_execution_env import BaseExecutionEnv
from gpt_computer.core.base_memory import BaseMemory
from gpt_computer.core.default.disk_execution_env import DiskExecutionEnv
from gpt_computer.core.default.disk_memory import DiskMemory
from gpt_computer.core.default.paths import PREPROMPTS_PATH, memory_path
from gpt_computer.core.default.steps import improve_fn as improve
from gpt_computer.core.files_dict import FilesDict
from gpt_computer.core.preprompts_holder import PrepromptsHolder
from gpt_computer.core.prompt import Prompt


def default_config_agent():
    """
    Creates an instance of PolyglotBenchmarkAgent with default configuration.

    Returns
    -------
    PolyglotBenchmarkAgent
    """
    return PolyglotBenchmarkAgent.with_default_config(tempfile.mkdtemp())


class PolyglotBenchmarkAgent:
    """
    A benchmark agent for polyglot programming exercises.

    This agent specializes in solving programming exercises across multiple languages
    from the Exercism curriculum. It can understand exercise requirements, generate
    solutions, and verify correctness.

    Attributes
    ----------
    memory : BaseMemory
        The memory interface where the code and related data are stored.
    execution_env : BaseExecutionEnv
        The execution environment in which the code is executed.
    ai : AI
        The AI model used for generating and improving code.
    preprompts_holder : PrepromptsHolder
        The holder for preprompt messages that guide the AI model.
    benchmark_runner : BenchmarkRunner
        The benchmark runner for evaluating exercises.
    """

    def __init__(
        self,
        memory: BaseMemory,
        execution_env: BaseExecutionEnv,
        ai: AI = None,
        preprompts_holder: PrepromptsHolder = None,
        benchmark_path: str = None,
    ):
        self.preprompts_holder = preprompts_holder or PrepromptsHolder(PREPROMPTS_PATH)
        self.memory = memory
        self.execution_env = execution_env
        self.ai = ai or AI(
            model_name=os.environ.get("MODEL_NAME", "gpt-4-turbo"),
        )

        # Initialize benchmark runner
        if benchmark_path is None:
            benchmark_path = os.path.dirname(os.path.abspath(__file__))
        self.benchmark_runner = BenchmarkRunner(benchmark_path)

        # Set up language executors
        self._setup_executors()

    def _setup_executors(self):
        """Set up language executors for supported languages."""
        self.benchmark_runner.add_executor("python", LanguageExecutor("python"))
        self.benchmark_runner.add_executor("javascript", LanguageExecutor("javascript"))
        self.benchmark_runner.add_executor("rust", LanguageExecutor("rust"))

    @classmethod
    def with_default_config(
        cls,
        path: str,
        ai: AI = None,
        preprompts_holder: PrepromptsHolder = None,
        benchmark_path: str = None,
    ):
        """
        Convenience method to create a PolyglotBenchmarkAgent with default configuration.
        :param path:
        :param ai:
        :param preprompts_holder:
        :param benchmark_path:
        :return: PolyglotBenchmarkAgent
        """
        return cls(
            memory=DiskMemory(memory_path(path)),
            execution_env=DiskExecutionEnv(),
            ai=ai,
            preprompts_holder=preprompts_holder or PrepromptsHolder(PREPROMPTS_PATH),
            benchmark_path=benchmark_path,
        )

    def improve(
        self,
        files_dict: FilesDict,
        prompt: Prompt,
        execution_command: Optional[str] = None,
    ) -> FilesDict:
        """
        Improve code for a programming exercise.

        This method analyzes the exercise requirements and generates or improves
        the solution code to pass all test cases.

        :param files_dict: Files containing the exercise code and tests
        :param prompt: The exercise description and requirements
        :param execution_command: Optional command for executing the code
        :return: Updated FilesDict with improved solution
        """

        # Extract exercise information from the prompt
        exercise_info = self._parse_exercise_prompt(prompt)

        # Create a specialized prompt for polyglot exercise solving
        specialized_prompt = self._create_exercise_prompt(exercise_info, files_dict)

        # Use the standard improve function with the specialized prompt
        files_dict = improve(
            self.ai, specialized_prompt, files_dict, self.memory, self.preprompts_holder
        )

        return files_dict

    def _parse_exercise_prompt(self, prompt: Prompt) -> dict:
        """
        Parse exercise information from the prompt.

        :param prompt: The exercise prompt
        :return: Dictionary containing exercise information
        """
        # This is a simplified implementation
        # In practice, you'd parse the prompt to extract:
        # - Programming language
        # - Exercise description
        # - Function signature
        # - Test cases
        # - Requirements

        return {
            "language": "python",  # Default, should be detected
            "description": str(prompt),
            "function_name": "solve",  # Default, should be detected
            "requirements": [],
        }

    def _create_exercise_prompt(
        self, exercise_info: dict, files_dict: FilesDict
    ) -> Prompt:
        """
        Create a specialized prompt for solving programming exercises.

        :param exercise_info: Parsed exercise information
        :param files_dict: Current files
        :return: Specialized prompt for exercise solving
        """
        prompt_template = f"""
You are solving a programming exercise for the {exercise_info['language']} track.

Exercise Description:
{exercise_info['description']}

Requirements:
1. Write correct, efficient, and readable code
2. Follow the language's best practices and conventions
3. Ensure your solution passes all test cases
4. Handle edge cases appropriately
5. Include proper error handling where needed

Current files:
{self._format_files_for_prompt(files_dict)}

Please analyze the exercise requirements and improve the solution code to pass all tests.
Focus on correctness first, then efficiency and readability.
"""

        return Prompt(prompt_template)

    def _format_files_for_prompt(self, files_dict: FilesDict) -> str:
        """Format files for inclusion in the prompt."""
        formatted = []
        for filename, content in files_dict.items():
            formatted.append(f"File: {filename}")
            formatted.append("```")
            formatted.append(content)
            formatted.append("```")
            formatted.append("")

        return "\n".join(formatted)

    def solve_exercise(self, exercise: Exercise) -> FilesDict:
        """
        Solve a specific exercise.

        :param exercise: The exercise to solve
        :return: FilesDict containing the solution
        """
        # Create initial files dict with starter code
        files_dict = FilesDict()

        if exercise.starter_code:
            # Determine file extension based on language
            extensions = {
                "python": "py",
                "javascript": "js",
                "rust": "rs",
                "java": "java",
                "cpp": "cpp",
            }
            ext = extensions.get(exercise.language, "txt")
            filename = f"solution.{ext}"
            files_dict[filename] = exercise.starter_code

        # Create prompt from exercise description
        prompt = Prompt(
            f"""
Solve this {exercise.language} programming exercise:

Title: {exercise.title}
Description: {exercise.description}

Topics: {', '.join(exercise.topics)}

Test Cases:
{self._format_test_cases(exercise.test_cases)}

Please provide a complete solution that passes all test cases.
"""
        )

        # Improve the solution
        solution_files = self.improve(files_dict, prompt)

        return solution_files

    def _format_test_cases(self, test_cases) -> str:
        """Format test cases for the prompt."""
        if not test_cases:
            return "No test cases provided."

        formatted = []
        for i, test_case in enumerate(test_cases, 1):
            formatted.append(f"Test {i}:")
            formatted.append(f"  Input: {test_case.input_data}")
            formatted.append(f"  Expected: {test_case.expected_output}")
            if test_case.description:
                formatted.append(f"  Description: {test_case.description}")
            formatted.append("")

        return "\n".join(formatted)

    def run_benchmark(
        self, track_filter: str = None, use_solution: bool = False
    ) -> dict:
        """
        Run the benchmark on exercises.

        :param track_filter: Optional filter for specific language tracks
        :param use_solution: Whether to use provided solutions instead of generated ones
        :return: Benchmark results
        """
        # Load exercises
        tracks = self.benchmark_runner.load_exercises()

        if track_filter:
            # Run only specific track
            if track_filter in tracks:
                self.benchmark_runner.run_track(tracks[track_filter], use_solution)
            else:
                raise ValueError(f"Track '{track_filter}' not found")
        else:
            # Run all tracks
            self.benchmark_runner.run_all(use_solution)

        return self.benchmark_runner.get_summary()
