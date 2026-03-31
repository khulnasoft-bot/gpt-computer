"""
Polyglot Benchmark - A curated collection of programming exercises from Exercism tracks.

This package provides a comprehensive benchmarking system for evaluating AI code generation
capabilities across multiple programming languages.
"""

from .benchmark_agent import PolyglotBenchmarkAgent, default_config_agent
from .benchmark_runner import (
    BenchmarkResult,
    BenchmarkRunner,
    ExecutionResult,
    LanguageExecutor,
)
from .exercise import Difficulty, Exercise, ExerciseStatus, ExerciseTrack, TestCase
from .loader import ExerciseLoader, ExercismImporter

__version__ = "1.0.0"
__author__ = "GPT-Computer Team"

__all__ = [
    # Core data structures
    "Exercise",
    "ExerciseTrack",
    "TestCase",
    "Difficulty",
    "ExerciseStatus",
    # Loading utilities
    "ExerciseLoader",
    "ExercismImporter",
    # Benchmark execution
    "BenchmarkRunner",
    "LanguageExecutor",
    "BenchmarkResult",
    "ExecutionResult",
    # GPT-Computer integration
    "PolyglotBenchmarkAgent",
    "default_config_agent",
]
