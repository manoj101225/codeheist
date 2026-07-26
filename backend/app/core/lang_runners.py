"""
Per-language compilation and execution runners for the CodeHeist judge.
Supports: Python, C++, Java, JavaScript.
"""

import subprocess
import tempfile
import os
import shutil
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

from app.core.config import JUDGE_TIMEOUT_MS


@dataclass
class RunResult:
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool
    execution_time_ms: float


class BaseRunner:
    language: str = ""

    def __init__(self, timeout_ms: Optional[int] = None):
        self.timeout_ms = timeout_ms or JUDGE_TIMEOUT_MS.get(self.language, 2000)
        self.work_dir = tempfile.mkdtemp(prefix=f"codeheist_{self.language}_")

    def cleanup(self):
        try:
            shutil.rmtree(self.work_dir, ignore_errors=True)
        except Exception:
            pass

    def _run_process(self, cmd: list[str], stdin_data: str = "") -> RunResult:
        import time
        timeout_sec = self.timeout_ms / 1000.0
        try:
            start = time.perf_counter()
            proc = subprocess.run(
                cmd,
                input=stdin_data,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                cwd=self.work_dir,
            )
            elapsed = (time.perf_counter() - start) * 1000
            return RunResult(
                stdout=proc.stdout.strip(),
                stderr=proc.stderr.strip(),
                exit_code=proc.returncode,
                timed_out=False,
                execution_time_ms=round(elapsed, 2),
            )
        except subprocess.TimeoutExpired:
            elapsed = self.timeout_ms
            return RunResult(
                stdout="",
                stderr=f"Time Limit Exceeded ({self.timeout_ms}ms)",
                exit_code=-1,
                timed_out=True,
                execution_time_ms=float(self.timeout_ms),
            )
        except Exception as e:
            return RunResult(
                stdout="",
                stderr=str(e),
                exit_code=-1,
                timed_out=False,
                execution_time_ms=0.0,
            )

    def compile(self, code: str, main_class: str = "Solution") -> Optional[str]:
        """Compile code if needed. Returns error string or None."""
        return None

    def execute(self, code: str, stdin_data: str = "", main_class: str = "Solution") -> RunResult:
        raise NotImplementedError


import sys

class PythonRunner(BaseRunner):
    language = "python"

    def execute(self, code: str, stdin_data: str = "", main_class: str = "Solution") -> RunResult:
        filepath = os.path.join(self.work_dir, "solution.py")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        return self._run_process([sys.executable, "-u", filepath], stdin_data)


class CppRunner(BaseRunner):
    language = "cpp"

    def compile(self, code: str, main_class: str = "Solution") -> Optional[str]:
        src = os.path.join(self.work_dir, "solution.cpp")
        self.exe = os.path.join(self.work_dir, "solution.exe" if os.name == "nt" else "solution")
        with open(src, "w", encoding="utf-8") as f:
            f.write(code)
        result = self._run_process(["g++", "-std=c++17", "-O2", "-o", self.exe, src])
        if result.exit_code != 0:
            return f"Compilation Error:\n{result.stderr}"
        return None

    def execute(self, code: str, stdin_data: str = "", main_class: str = "Solution") -> RunResult:
        if not hasattr(self, "exe"):
            err = self.compile(code, main_class)
            if err:
                return RunResult(stdout="", stderr=err, exit_code=-1, timed_out=False, execution_time_ms=0.0)
        return self._run_process([self.exe], stdin_data)


class JavaRunner(BaseRunner):
    language = "java"

    def compile(self, code: str, main_class: str = "Solution") -> Optional[str]:
        src = os.path.join(self.work_dir, "Solution.java")
        self.main_class = main_class
        with open(src, "w", encoding="utf-8") as f:
            f.write(code)
        result = self._run_process(["javac", src])
        if result.exit_code != 0:
            return f"Compilation Error:\n{result.stderr}"
        return None

    def execute(self, code: str, stdin_data: str = "", main_class: str = "Solution") -> RunResult:
        if not hasattr(self, "_compiled"):
            err = self.compile(code, main_class)
            if err:
                return RunResult(stdout="", stderr=err, exit_code=-1, timed_out=False, execution_time_ms=0.0)
            self._compiled = True
        entry_class = getattr(self, "main_class", main_class)
        return self._run_process(["java", "-cp", self.work_dir, entry_class], stdin_data)


class JSRunner(BaseRunner):
    language = "javascript"

    def execute(self, code: str, stdin_data: str = "", main_class: str = "Solution") -> RunResult:
        if os.name == "nt":
            code = code.replace("'/dev/stdin'", "0").replace('"/dev/stdin"', "0")
        filepath = os.path.join(self.work_dir, "solution.js")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        return self._run_process(["node", filepath], stdin_data)


RUNNERS = {
    "python": PythonRunner,
    "cpp": CppRunner,
    "java": JavaRunner,
    "javascript": JSRunner,
}


def get_runner(language: str, timeout_ms: Optional[int] = None) -> BaseRunner:
    runner_cls = RUNNERS.get(language)
    if not runner_cls:
        raise ValueError(f"Unsupported language: {language}. Supported: {list(RUNNERS.keys())}")
    return runner_cls(timeout_ms)
