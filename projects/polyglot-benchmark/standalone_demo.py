#!/usr/bin/env python3
"""
Standalone demo script for the polyglot benchmark system.
This version doesn't depend on gpt_computer modules.
"""

from pathlib import Path

from benchmark_runner import BenchmarkRunner, LanguageExecutor
from exercise import Difficulty, Exercise, ExerciseTrack, TestCase
from loader import ExerciseLoader


def main():
    """Run a demonstration of the polyglot benchmark system."""
    print("🚀 Polyglot Benchmark Demo (Standalone)")
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

    # Run benchmark on solution code (only for languages we can execute)
    print("\n🏃 Running benchmark on solution code...")
    runner = BenchmarkRunner(base_path)

    # Add executors for languages we can test
    runner.add_executor("python", LanguageExecutor("python"))
    runner.add_executor("javascript", LanguageExecutor("javascript"))

    # Note: Rust executor requires cargo to be installed, so we'll skip it for now
    print("Note: Rust execution requires cargo to be installed")

    # Run exercises for supported languages
    results = []
    for lang, track in tracks.items():
        if lang in [
            "python",
            "javascript",
        ]:  # Only test languages we have executors for
            print(f"\nRunning {lang} exercises...")
            for exercise in track.exercises:
                try:
                    result = runner.run_exercise(exercise, use_solution=True)
                    results.append(result)
                    runner.results.append(result)  # Add to runner's results list
                    status = "✅" if result.execution_result.value == "success" else "❌"
                    print(f"  {status} {exercise.slug}")
                except Exception as e:
                    print(f"  ❌ {exercise.slug}: {e}")

    # Display results
    if results:
        print("\n📊 Benchmark Results:")
        print(f"Total exercises tested: {len(results)}")

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
            else:
                print(
                    f"   Output: {result.output[:100]}..."
                )  # Show first 100 chars of output

        # Save results
        results_file = base_path / "standalone_demo_results.json"
        runner.save_results(str(results_file))
        print(f"\n💾 Results saved to: {results_file}")

        # Show summary
        summary = runner.get_summary()
        if summary:
            print("\n📈 Summary:")
            print(f"Overall success rate: {summary['overall_success_rate']:.1%}")
            print(
                f"Overall test success rate: {summary['overall_test_success_rate']:.1%}"
            )

            if "language_stats" in summary:
                print("\nLanguage Statistics:")
                for lang, stats in summary["language_stats"].items():
                    print(f"  {lang}:")
                    print(f"    Success rate: {stats['success_rate']:.1%}")
                    print(f"    Test success rate: {stats['test_success_rate']:.1%}")
                    print(f"    Average time: {stats['avg_time']:.3f}s")
        else:
            print("\n📈 Summary: No results to display")
    else:
        print("\n⚠️  No exercises were executed. This might be due to:")
        print("   - Missing runtime environments (python3, node)")
        print("   - Missing dependencies")
        print("   - Execution errors")


def test_exercise_structures():
    """Test the exercise data structures."""
    print("\n🧪 Testing Exercise Data Structures")
    print("=" * 40)

    # Create a test exercise
    test_case = TestCase(
        input_data=["Alice"],
        expected_output="One for Alice, one for me.",
        description="Test with name Alice",
    )

    exercise = Exercise(
        slug="test-exercise",
        language="python",
        track="python",
        title="Test Exercise",
        description="A test exercise for demonstration",
        difficulty=Difficulty.EASY,
        test_cases=[test_case],
        topics=["strings", "functions"],
    )

    print("✅ Created test exercise:")
    print(f"   Slug: {exercise.slug}")
    print(f"   Title: {exercise.title}")
    print(f"   Language: {exercise.language}")
    print(f"   Difficulty: {exercise.difficulty.value}")
    print(f"   Test cases: {len(exercise.test_cases)}")

    # Test serialization
    exercise_dict = exercise.to_dict()
    Exercise.from_dict(exercise_dict)

    print("✅ Serialization test passed")

    # Test track
    ExerciseTrack(language="python", track_id="python", exercises=[exercise])

    print("✅ Created test track with {len(track.exercises)} exercises")

    # Test JSON
    json_str = exercise.to_json()
    Exercise.from_json(json_str)

    print("✅ JSON serialization test passed")


if __name__ == "__main__":
    test_exercise_structures()
    main()
