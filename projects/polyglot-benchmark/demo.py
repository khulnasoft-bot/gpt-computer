#!/usr/bin/env python3
"""
Demo script for the polyglot benchmark system.
"""

from pathlib import Path

from benchmark_agent import PolyglotBenchmarkAgent
from benchmark_runner import BenchmarkRunner, LanguageExecutor
from loader import ExerciseLoader


def main():
    """Run a demonstration of the polyglot benchmark system."""
    print("🚀 Polyglot Benchmark Demo")
    print("=" * 50)

    # Get the current directory
    base_path = Path(__file__).parent

    # Load exercises
    print("\n📚 Loading exercises...")
    loader = ExerciseLoader(base_path)
    tracks = loader.load_all_tracks()

    print(f"Loaded {len(tracks)} language tracks:")
    for lang, track in tracks.items():
        print(f"  - {lang}: {len(track.exercises)} exercises")

    # Display exercise details
    print("\n📋 Exercise Details:")
    for lang, track in tracks.items():
        print(f"\n{lang.upper()} Track:")
        for exercise in track.exercises[:3]:  # Show first 3 exercises
            print(f"  - {exercise.title} ({exercise.slug})")
            print(f"    Difficulty: {exercise.difficulty.value}")
            print(f"    Topics: {', '.join(exercise.topics)}")
            print(f"    Test cases: {len(exercise.test_cases)}")

    # Run benchmark on solution code
    print("\n🏃 Running benchmark on solution code...")
    runner = BenchmarkRunner(base_path)

    # Add executors
    runner.add_executor("python", LanguageExecutor("python"))
    runner.add_executor("javascript", LanguageExecutor("javascript"))
    # Note: Rust executor requires cargo to be installed
    # runner.add_executor("rust", LanguageExecutor("rust"))

    # Run all exercises
    results = runner.run_all(use_solution=True)

    # Display results
    print("\n📊 Benchmark Results:")
    print(f"Total exercises: {len(results)}")

    successful = sum(1 for r in results if r.execution_result.value == "success")
    print(f"Successful: {successful}")
    print(f"Failed: {len(results) - successful}")

    # Show detailed results
    print("\n🔍 Detailed Results:")
    for result in results:
        status = "✅" if result.execution_result.value == "success" else "❌"
        print(f"{status} {result.exercise.language}/{result.exercise.slug}")
        print(f"   Time: {result.execution_time:.3f}s")
        if result.test_results:
            passed = sum(result.test_results)
            total = len(result.test_results)
            print(f"   Tests: {passed}/{total} passed")
        if result.error:
            print(f"   Error: {result.error}")

    # Save results
    results_file = base_path / "demo_results.json"
    runner.save_results(str(results_file))
    print(f"\n💾 Results saved to: {results_file}")

    # Show summary
    summary = runner.get_summary()
    print("\n📈 Summary:")
    print(f"Overall success rate: {summary['overall_success_rate']:.1%}")
    print(f"Overall test success rate: {summary['overall_test_success_rate']:.1%}")

    if "language_stats" in summary:
        print("\nLanguage Statistics:")
        for lang, stats in summary["language_stats"].items():
            print(f"  {lang}:")
            print(f"    Success rate: {stats['success_rate']:.1%}")
            print(f"    Test success rate: {stats['test_success_rate']:.1%}")
            print(f"    Average time: {stats['avg_time']:.3f}s")


def demo_agent():
    """Demonstrate the benchmark agent capabilities."""
    print("\n🤖 Benchmark Agent Demo")
    print("=" * 50)

    # Create agent
    agent = PolyglotBenchmarkAgent.with_default_config("/tmp/polyglot_demo")

    # Load exercises
    tracks = agent.benchmark_runner.load_exercises()

    # Solve one exercise as demo
    python_track = tracks.get("python")
    if python_track and python_track.exercises:
        exercise = python_track.exercises[0]
        print(f"\n🎯 Solving exercise: {exercise.title}")
        print(f"Language: {exercise.language}")
        print(f"Description: {exercise.description}")

        try:
            solution_files = agent.solve_exercise(exercise)
            print("\n✅ Solution generated:")
            for filename, content in solution_files.items():
                print(f"  {filename}:")
                print("  " + "\n  ".join(content.split("\n")[:5]))
                if len(content.split("\n")) > 5:
                    print("  ...")
        except Exception as e:
            print(f"\n❌ Error solving exercise: {e}")


if __name__ == "__main__":
    main()
    demo_agent()
