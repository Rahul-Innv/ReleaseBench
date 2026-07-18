#!/usr/bin/env python3
"""Run ReleaseBench atomic-family tests with deterministic output."""

from __future__ import annotations

import os
import unittest
from pathlib import Path


EXPECTED_TEST_COUNT = 19


def result_contract_violations(
    *,
    tests_run: int,
    failures: int,
    errors: int,
    skipped: int,
) -> tuple[str, ...]:
    """Return deterministic reasons a focused-suite result is not exact."""

    violations: list[str] = []
    if tests_run != EXPECTED_TEST_COUNT:
        violations.append(f"tests expected={EXPECTED_TEST_COUNT} actual={tests_run}")
    if skipped:
        violations.append(f"skipped expected=0 actual={skipped}")
    if failures:
        violations.append(f"failures expected=0 actual={failures}")
    if errors:
        violations.append(f"errors expected=0 actual={errors}")
    return tuple(violations)


def main() -> int:
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    os.environ.setdefault("PYTHONHASHSEED", "0")
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).parent), pattern="test_*.py")
    result = unittest.TestResult()
    suite.run(result)
    for test, detail in [*result.failures, *result.errors]:
        print(f"FAIL {test.id()}")
        print(detail.rstrip())
    print(
        "releasebench-atomic-tests "
        f"tests={result.testsRun} failures={len(result.failures)} "
        f"errors={len(result.errors)} skipped={len(result.skipped)}"
    )
    print("candidate_root=.")
    violations = result_contract_violations(
        tests_run=result.testsRun,
        failures=len(result.failures),
        errors=len(result.errors),
        skipped=len(result.skipped),
    )
    for violation in violations:
        print(f"CONTRACT_FAIL {violation}")
    passed = result.wasSuccessful() and not violations
    print("PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
