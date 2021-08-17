#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess  # nosec
import sys

from flake8.main import git
from isort.hooks import git_hook as isort_githook

from src.core.utils import cowsay


def run_ci_checks() -> None:
    _check_missing_django_migrations()
    _run_tests()
    _check_imports_order_with_isort()
    _check_code_formatting_with_black()
    _check_code_style_with_flake8()
    _check_security_issues_with_bandit()
    _check_python_packages_safety()


def _run_tests() -> None:
    cowsay("Run test suite with pytest")
    pytests_cmd = ["tusk", "tests:run", "--reuse-db=false"]
    tests_return_code = subprocess.run(pytests_cmd).returncode  # nosec
    # Exit code 0: All tests were collected and passed successfully.
    # Exit code 5: No tests were collected.
    if tests_return_code not in {0, 5}:
        print("")
        print(f"Tests Exit Status: {tests_return_code} => aborting commit!")
        sys.exit(tests_return_code)


def _check_missing_django_migrations() -> None:
    cowsay("Check missing Django migrations")
    dj_makemigrations_command = ["tusk", "ci:check-missing-dj-migrations"]
    dj_makemigrations_return_code = subprocess.run(dj_makemigrations_command).returncode  # nosec
    if dj_makemigrations_return_code == 0:
        print("")
        print("Django makemigrations Exit Status: 0 => OK!")
    else:
        print("")
        print(f"Django makemigrations Status: {dj_makemigrations_return_code} => aborting commit!")
        sys.exit(dj_makemigrations_return_code)


def _check_imports_order_with_isort() -> None:
    cowsay("Check imports order with Isort")
    isort_exit_status = isort_githook(strict=True)
    if isort_exit_status == 0:
        print("Isort Exit Status: 0 => OK!")
    else:
        sys.exit(isort_exit_status)


def _check_code_formatting_with_black() -> None:
    cowsay("Check code formatting with Black")
    black_cmd = ["black", "--line-length=100", "--exclude=venv", "--check", "."]
    black_return_code = subprocess.run(black_cmd).returncode  # nosec
    if black_return_code == 0:
        print("")
        print("Black Exit Status: 0 => OK!")
    else:
        print("")
        print(f"Black Exit Status: {black_return_code} => aborting commit!")
        print("")
        sys.exit(black_return_code)


def _check_code_style_with_flake8() -> None:
    cowsay("Check code style with Flake8")
    flake8_return_code = git.hook(strict=git.config_for("strict"), lazy=git.config_for("lazy"))
    if flake8_return_code == 0:
        print("Flake8 Exit Status: 0 => OK!")
        print("")
    else:
        print("")
        print(f"Flake8 Exit Status: {flake8_return_code} => aborting commit!")
        print("")
        sys.exit(flake8_return_code)


def _check_security_issues_with_bandit() -> None:
    cowsay("Check security issues with Bandit")
    bandit_command = ["bandit", "--recursive", "--exclude=/app_tests,/tests,/venv", "."]
    bandit_return_code = subprocess.run(bandit_command).returncode  # nosec
    if bandit_return_code == 0:
        print("Bandit Exit Status: 0 => OK!")
    else:
        print("")
        print(f"Bandit Exit Status: {bandit_return_code} => aborting commit!")
        print("")
        sys.exit(bandit_return_code)


def _check_python_packages_safety() -> None:
    cowsay("Check Python packages with Safety")
    safety_command = ["safety", "check", "--file", "requirements/locked/dev.txt"]
    safety_return_code = subprocess.run(safety_command).returncode  # nosec
    if safety_return_code == 0:
        print("")
        print("Safety Exit Status: 0 => OK!")
    else:
        print("")
        print(f"Safety Exit Status: {safety_return_code} => aborting commit!")
        sys.exit(safety_return_code)


if __name__ == "__main__":
    run_ci_checks()
