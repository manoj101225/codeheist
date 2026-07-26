"""
CodeHeist Judge — runs user code against test cases across all supported languages.
"""

from dataclasses import dataclass
from typing import Optional

from app.core.lang_runners import get_runner, RunResult
from app.core.harness import apply_harness


@dataclass
class TestResult:
    test_index: int
    passed: bool
    input_data: str
    expected: str
    actual: str
    execution_time_ms: float
    error: str = ""


@dataclass
class JudgeVerdict:
    status: str  # "passed", "failed", "error", "timeout", "compile_error"
    tests_passed: int
    tests_total: int
    results: list[TestResult]
    total_time_ms: float
    error_message: str = ""


def judge_submission(
    code: str,
    language: str,
    test_cases: list[dict],  # [{"input": "...", "expected": "..."}]
    mission_title: str = "",
    timeout_ms: Optional[int] = None,
) -> JudgeVerdict:
    """
    Execute user code against all test cases and return a verdict.
    Each test case provides input via stdin and compares stdout to expected output.
    """
    runner = get_runner(language, timeout_ms)
    results: list[TestResult] = []
    tests_passed = 0
    total_time = 0.0

    # Wrap LeetCode-style solution with harness driver
    executable_code, main_class = apply_harness(code, language, mission_title)

    try:
        # Compile step (for C++ and Java)
        compile_err = runner.compile(executable_code, main_class=main_class)
        if compile_err:
            return JudgeVerdict(
                status="compile_error",
                tests_passed=0,
                tests_total=len(test_cases),
                results=[],
                total_time_ms=0.0,
                error_message=compile_err,
            )

        # Run each test case
        for i, tc in enumerate(test_cases):
            run_result: RunResult = runner.execute(executable_code, tc["input"], main_class=main_class)
            total_time += run_result.execution_time_ms

            if run_result.timed_out:
                results.append(TestResult(
                    test_index=i,
                    passed=False,
                    input_data=tc["input"],
                    expected=tc["expected"],
                    actual="",
                    execution_time_ms=run_result.execution_time_ms,
                    error="Time Limit Exceeded",
                ))
                # On TLE, fail remaining tests
                for j in range(i + 1, len(test_cases)):
                    results.append(TestResult(
                        test_index=j,
                        passed=False,
                        input_data=test_cases[j]["input"],
                        expected=test_cases[j]["expected"],
                        actual="",
                        execution_time_ms=0.0,
                        error="Skipped (previous TLE)",
                    ))
                return JudgeVerdict(
                    status="timeout",
                    tests_passed=tests_passed,
                    tests_total=len(test_cases),
                    results=results,
                    total_time_ms=round(total_time, 2),
                    error_message="Time Limit Exceeded",
                )

            if run_result.exit_code != 0:
                results.append(TestResult(
                    test_index=i,
                    passed=False,
                    input_data=tc["input"],
                    expected=tc["expected"],
                    actual=run_result.stdout,
                    execution_time_ms=run_result.execution_time_ms,
                    error=run_result.stderr[:500],
                ))
            else:
                # Compare output (strip whitespace for flexible comparison)
                actual = run_result.stdout.strip()
                expected = tc["expected"].strip()
                passed = actual == expected

                if passed:
                    tests_passed += 1

                results.append(TestResult(
                    test_index=i,
                    passed=passed,
                    input_data=tc["input"],
                    expected=expected,
                    actual=actual,
                    execution_time_ms=run_result.execution_time_ms,
                    error="" if passed else "Wrong Answer",
                ))

        # Final verdict
        all_passed = tests_passed == len(test_cases)
        status = "passed" if all_passed else "failed"
        has_errors = any(r.error and r.error not in ("Wrong Answer",) for r in results)
        if has_errors and not all_passed:
            status = "error"

        return JudgeVerdict(
            status=status,
            tests_passed=tests_passed,
            tests_total=len(test_cases),
            results=results,
            total_time_ms=round(total_time, 2),
        )

    finally:
        runner.cleanup()
