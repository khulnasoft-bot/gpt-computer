# GPT-Computer - Polyglot Benchmark

A curated collection of programming exercises extracted from Exercism's language tracks, designed for benchmarking and testing AI code generation capabilities across multiple programming languages.

## Overview

This benchmark provides a standardized way to evaluate how well AI systems can understand and solve programming problems in different languages. It includes exercises from Exercism, a well-established platform for learning programming through practice problems.

## Features

- **Multi-language Support**: Exercises in Python, JavaScript, Rust, and more
- **Standardized Format**: Consistent structure for exercises across all languages
- **Automated Testing**: Built-in test case execution and validation
- **Benchmark Runner**: Comprehensive performance evaluation
- **GPT-Computer Integration**: Seamless integration with the GPT-Computer benchmarking framework

## Architecture

### Core Components

1. **Exercise Data Structures** (`exercise.py`)
   - `Exercise`: Represents a single programming exercise
   - `ExerciseTrack`: Collection of exercises for a language
   - `TestCase`: Individual test case with input/output

2. **Exercise Loader** (`loader.py`)
   - Loads exercises from directory structure
   - Supports JSON/YAML metadata formats
   - Exercism format import capabilities

3. **Benchmark Runner** (`benchmark_runner.py`)
   - Executes exercises across multiple languages
   - Measures performance and correctness
   - Generates detailed reports

4. **Benchmark Agent** (`benchmark_agent.py`)
   - GPT-Computer compatible agent
   - Solves exercises using AI
   - Integrates with existing benchmark infrastructure

## Directory Structure

```
polyglot-benchmark/
├── README.md                 # This file
├── exercise.py              # Core data structures
├── loader.py                # Exercise loading utilities
├── benchmark_runner.py      # Execution and evaluation
├── benchmark_agent.py       # GPT-Computer integration
├── bench_config.toml        # Benchmark configuration
├── demo.py                  # Demonstration script
├── python/                  # Python exercises
│   ├── track_metadata.json
│   └── exercises/
│       └── two-fer/
│           ├── metadata.json
│           ├── starter.py
│           ├── solution.py
│           └── test_cases.json
├── javascript/              # JavaScript exercises
│   ├── track_metadata.json
│   └── exercises/
│       └── leap/
│           ├── metadata.json
│           ├── starter.js
│           ├── solution.js
│           └── test_cases.json
└── rust/                   # Rust exercises
    ├── track_metadata.json
    └── exercises/
        └── gigasecond/
            ├── metadata.json
            ├── starter.rs
            ├── solution.rs
            └── test_cases.json
```

## Exercise Format

Each exercise follows a standardized structure:

### Metadata (`metadata.json`)
```json
{
  "slug": "exercise-name",
  "title": "Exercise Title",
  "description": "Exercise description",
  "difficulty": "easy|medium|hard",
  "topics": ["topic1", "topic2"],
  "prerequisites": ["prereq1"],
  "uuid": "unique-identifier"
}
```

### Starter Code (`starter.{ext}`)
Template code with function signatures and placeholders for implementation.

### Solution Code (`solution.{ext}`)
Reference implementation that passes all test cases.

### Test Cases (`test_cases.json`)
```json
[
  {
    "input": ["param1", "param2"],
    "expected": "expected_output",
    "description": "Test description"
  }
]
```

## Usage

### Running the Demo

```bash
cd projects/polyglot-benchmark
python demo.py
```

This will:
1. Load all exercises from the configured tracks
2. Run benchmarks using the provided solutions
3. Display performance metrics and results
4. Save detailed results to `demo_results.json`

### Using the Benchmark Agent

```python
from benchmark_agent import PolyglotBenchmarkAgent

# Create agent
agent = PolyglotBenchmarkAgent.with_default_config("/tmp/benchmark")

# Solve exercises
tracks = agent.benchmark_runner.load_exercises()
for track in tracks.values():
    for exercise in track.exercises:
        solution = agent.solve_exercise(exercise)
        # Process solution...
```

### Running Benchmarks

```python
from benchmark_runner import BenchmarkRunner, LanguageExecutor

# Create runner
runner = BenchmarkRunner("/path/to/exercises")
runner.add_executor("python", LanguageExecutor("python"))

# Run all exercises
results = runner.run_all(use_solution=True)

# Get summary
summary = runner.get_summary()
print(f"Success rate: {summary['overall_success_rate']:.1%}")
```

## Adding New Exercises

### 1. Create Exercise Directory
```bash
mkdir -p python/exercises/new-exercise
```

### 2. Add Metadata
Create `python/exercises/new-exercise/metadata.json` with exercise information.

### 3. Add Starter Code
Create `python/exercises/new-exercise/starter.py` with the function signature.

### 4. Add Solution
Create `python/exercises/new-exercise/solution.py` with the correct implementation.

### 5. Add Test Cases
Create `python/exercises/new-exercise/test_cases.json` with test data.

## Adding New Languages

### 1. Create Language Directory
```bash
mkdir new-language
```

### 2. Add Track Metadata
Create `new-language/track_metadata.json`.

### 3. Add Exercises
Follow the same structure as existing languages.

### 4. Update Language Executor
Add execution support in `benchmark_runner.py`:

```python
def _execute_new_language(self, code: str, test_cases: List[TestCase]):
    # Implementation for new language
    pass
```

## Configuration

The benchmark behavior is controlled by `bench_config.toml`:

```toml
[python]
active = true
difficulty = ["easy", "medium", "hard"]
topics = ["strings", "conditionals", "functions"]

[general]
timeout_seconds = 30
max_exercises_per_language = 20
```

## Integration with GPT-Computer

This benchmark is designed to work seamlessly with the GPT-Computer framework:

1. **Standard Interface**: Implements the required `improve()` method
2. **File Management**: Uses `FilesDict` for code handling
3. **Memory Integration**: Compatible with GPT-Computer memory systems
4. **Execution Environment**: Works with standard execution environments

## Performance Metrics

The benchmark tracks multiple metrics:

- **Success Rate**: Percentage of exercises solved correctly
- **Test Pass Rate**: Percentage of test cases passed
- **Execution Time**: Time taken to generate solutions
- **Language Coverage**: Performance across different languages

## Contributing

To add new exercises or improve the benchmark:

1. Follow the established exercise format
2. Ensure all test cases are comprehensive
3. Test with the demo script
4. Update documentation as needed

## License

This benchmark follows the same license as the GPT-Computer project.
