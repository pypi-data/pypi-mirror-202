import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from rich.traceback import Trace

import briefcase
from briefcase.console import Log
from briefcase.exceptions import BriefcaseError

TRACEBACK_HEADER = "Traceback (most recent call last)"
EXTRA_HEADER = "Extra information:"


@pytest.fixture
def now(monkeypatch):
    """monkeypatch the datetime.now inside of briefcase.console."""
    now = datetime.datetime(2022, 6, 25, 16, 12, 29)
    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = now
    monkeypatch.setattr(briefcase.console, "datetime", datetime_mock)
    return now


def test_capture_stacktrace():
    """capture_stacktrace sets Log.stacktrace."""
    logger = Log()
    assert logger.skip_log is False

    try:
        1 / 0
    except ZeroDivisionError:
        logger.capture_stacktrace()

    assert len(logger.stacktraces) == 1
    assert logger.stacktraces[0][0] == "Main thread"
    assert isinstance(logger.stacktraces[0][1], Trace)
    assert logger.skip_log is False


@pytest.mark.parametrize("skip_logfile", [True, False])
def test_capture_stacktrace_for_briefcaseerror(skip_logfile):
    """skip_log is updated for BriefcaseError exceptions."""
    logger = Log()
    assert logger.skip_log is False

    try:
        raise BriefcaseError(error_code=542, skip_logfile=skip_logfile)
    except BriefcaseError:
        logger.capture_stacktrace()

    assert len(logger.stacktraces) == 1
    assert logger.stacktraces[0][0] == "Main thread"
    assert isinstance(logger.stacktraces[0][1], Trace)
    assert logger.skip_log is skip_logfile


def test_save_log_to_file_do_not_log():
    """Nothing is done to save log if no command or --log wasn't passed."""
    logger = Log()
    logger.save_log_to_file(command=None)

    command = MagicMock()
    logger.save_log = False
    logger.save_log_to_file(command=command)
    command.input.wait_bar.assert_not_called()

    # There were no stack traces captured
    assert len(logger.stacktraces) == 0


def test_save_log_to_file_no_exception(tmp_path, now):
    """Log file contains everything printed to log; env vars are sanitized; no
    stacktrace if one is not captured."""
    command = MagicMock()
    command.base_path = Path(tmp_path)
    command.command = "dev"
    command.tools.os.environ = {
        "GITHUB_KEY": "super-secret-key",
        "ANDROID_SDK_ROOT": "/androidsdk",
    }

    logger = Log(verbosity=2)
    logger.save_log = True
    logger.debug("this is debug output")
    logger.info("this is info output")
    logger.warning("this is warning output")
    logger.error("this is error output")
    logger.print("this is print output")
    logger.print.to_log("this is log output")
    logger.print.to_console("this is console output")

    logger.info("this is [bold]info output with markup[/bold]")
    logger.info(
        "this is [bold]info output with markup and a prefix[/bold]", prefix="wibble"
    )
    logger.info("this is [bold]info output with escaped markup[/bold]", markup=True)
    logger.info(
        "this is [bold]info output with escaped markup and a prefix[/bold]",
        prefix="wibble",
        markup=True,
    )
    logger.save_log_to_file(command=command)

    log_filepath = tmp_path / "logs" / "briefcase.2022_06_25-16_12_29.dev.log"

    assert log_filepath.exists()
    with open(log_filepath, encoding="utf-8") as log:
        log_contents = log.read()

    assert log_contents.startswith("Date/Time:       2022-06-25 16:12:29")
    assert ">>> this is debug output" in log_contents
    assert "this is info output" in log_contents
    assert "this is [bold]info output with markup[/bold]" in log_contents
    assert "this is info output with escaped markup" in log_contents
    assert "this is warning output" in log_contents
    assert "this is error output" in log_contents
    assert "this is print output" in log_contents
    assert "this is log output" in log_contents
    assert "this is console output" not in log_contents
    # Environment variables are in the output
    assert "ANDROID_SDK_ROOT=/androidsdk" in log_contents
    assert "GITHUB_KEY=********************" in log_contents
    assert "GITHUB_KEY=super-secret-key" not in log_contents
    # Environment variables are sorted
    assert log_contents.index("ANDROID_SDK_ROOT") < log_contents.index("GITHUB_KEY")

    assert TRACEBACK_HEADER not in log_contents
    assert EXTRA_HEADER not in log_contents


def test_save_log_to_file_with_exception(tmp_path, now):
    """Log file contains exception stacktrace when one is captured."""
    command = MagicMock()
    command.base_path = Path(tmp_path)
    command.command = "dev"
    command.tools.os.environ = {}

    logger = Log()
    logger.save_log = True
    try:
        1 / 0
    except ZeroDivisionError:
        logger.capture_stacktrace()
    logger.save_log_to_file(command=command)

    log_filepath = tmp_path / "logs" / "briefcase.2022_06_25-16_12_29.dev.log"

    assert log_filepath.exists()
    with open(log_filepath, encoding="utf-8") as log:
        log_contents = log.read()

    assert len(logger.stacktraces) == 1
    assert log_contents.startswith("Date/Time:       2022-06-25 16:12:29")
    assert TRACEBACK_HEADER in log_contents
    assert log_contents.splitlines()[-1].startswith("ZeroDivisionError")


def test_save_log_to_file_with_multiple_exceptions(tmp_path, now):
    """Log file contains exception stacktrace when more than one is captured."""
    command = MagicMock()
    command.base_path = Path(tmp_path)
    command.command = "dev"
    command.tools.os.environ = {}

    logger = Log()
    logger.save_log = True
    for i in range(1, 5):
        try:
            1 / 0
        except ZeroDivisionError:
            logger.capture_stacktrace(f"Thread {i}")

    logger.save_log_to_file(command=command)

    log_filepath = tmp_path / "logs" / "briefcase.2022_06_25-16_12_29.dev.log"

    assert log_filepath.exists()
    with open(log_filepath, encoding="utf-8") as log:
        log_contents = log.read()

    assert len(logger.stacktraces) == 4
    assert log_contents.startswith("Date/Time:       2022-06-25 16:12:29")
    assert TRACEBACK_HEADER in log_contents
    for i in range(1, 5):
        assert f"\nThread {i} traceback:\n" in log_contents
    assert log_contents.splitlines()[-1].startswith("ZeroDivisionError")


def test_save_log_to_file_extra(tmp_path, now):
    """Log file extras are called when the log is written."""
    command = MagicMock()
    command.base_path = Path(tmp_path)
    command.command = "dev"

    logger = Log()
    logger.save_log = True

    def extra1():
        logger.debug("Log extra 1")

    def extra2():
        raise ValueError("Log extra 2")

    def extra3():
        logger.debug("Log extra 3")

    for extra in [extra1, extra2, extra3]:
        logger.add_log_file_extra(extra)
    logger.save_log_to_file(command=command)
    log_filepath = tmp_path / "logs" / "briefcase.2022_06_25-16_12_29.dev.log"
    with open(log_filepath, encoding="utf-8") as log:
        log_contents = log.read()

    assert EXTRA_HEADER in log_contents
    assert "Log extra 1" in log_contents
    assert TRACEBACK_HEADER in log_contents
    assert "ValueError: Log extra 2" in log_contents
    assert "Log extra 3" in log_contents


def test_save_log_to_file_extra_interrupted(tmp_path, now):
    """Log file extras can be interrupted by Ctrl-C."""
    command = MagicMock()
    command.base_path = Path(tmp_path)
    command.command = "dev"

    logger = Log()
    logger.save_log = True

    def extra1():
        raise KeyboardInterrupt()

    extra2 = MagicMock()
    for extra in [extra1, extra2]:
        logger.add_log_file_extra(extra)
    with pytest.raises(KeyboardInterrupt):
        logger.save_log_to_file(command=command)
    extra2.assert_not_called()
    log_filepath = tmp_path / "logs" / "briefcase.2022_06_25-16_12_29.dev.log"
    assert log_filepath.stat().st_size == 0


def test_save_log_to_file_fail_to_write_file(capsys):
    """User is informed when the log file cannot be written."""
    command = MagicMock()
    command.base_path = Path("/a-path-that-will-cause-an-OSError...")
    command.command = "dev"
    command.tools.os.environ = {}

    logger = Log()
    logger.save_log = True

    logger.print("a line of output")
    logger.save_log_to_file(command=command)

    last_line_of_output = capsys.readouterr().out.strip().splitlines()[-1]
    assert last_line_of_output.startswith("Failed to save log to ")


def test_log_with_context(tmp_path, capsys):
    """Log file can be given a persistent context."""
    command = MagicMock()
    command.base_path = Path(tmp_path)

    logger = Log(verbosity=2)
    logger.save_log = False

    logger.info("this is info output")
    with logger.context("Deep"):
        logger.info("this is deep context")
        logger.info("prefixed deep context", prefix="prefix")
        logger.info()
        logger.debug("this is deep debug")
        with logger.context("Really Deep"):
            logger.info("this is really deep context")
            logger.info("prefixed really deep context", prefix="prefix2")
            logger.info()
            logger.debug("this is really deep debug")
        logger.info("Pop back to deep")
    logger.info("Pop back to normal")

    assert capsys.readouterr().out == "\n".join(
        [
            "this is info output",
            "",
            "Entering Deep context...",
            "Deep| --------------------------------------------------------------------",
            "Deep| this is deep context",
            "Deep| ",
            "Deep| [prefix] prefixed deep context",
            "Deep| ",
            "Deep| >>> this is deep debug",
            "Deep| ",
            "Deep| Entering Really Deep context...",
            "Really Deep| -------------------------------------------------------------",
            "Really Deep| this is really deep context",
            "Really Deep| ",
            "Really Deep| [prefix2] prefixed really deep context",
            "Really Deep| ",
            "Really Deep| >>> this is really deep debug",
            "Really Deep| -------------------------------------------------------------",
            "Deep| Leaving Really Deep context.",
            "Deep| ",
            "Deep| Pop back to deep",
            "Deep| --------------------------------------------------------------------",
            "Leaving Deep context.",
            "",
            "Pop back to normal",
            "",
        ]
    )


def test_log_error_with_context_(tmp_path, capsys):
    """If an exception is raised in a logging context, the context is cleared."""
    command = MagicMock()
    command.base_path = Path(tmp_path)

    logger = Log(verbosity=2)
    logger.save_log = False

    logger.info("this is info output")
    try:
        with logger.context("Deep"):
            logger.info("this is deep context")
            raise ValueError()
    except ValueError:
        logger.info("this is cleanup")

    assert capsys.readouterr().out == "\n".join(
        [
            "this is info output",
            "",
            "Entering Deep context...",
            "Deep| --------------------------------------------------------------------",
            "Deep| this is deep context",
            "Deep| --------------------------------------------------------------------",
            "Leaving Deep context.",
            "",
            "this is cleanup",
            "",
        ]
    )
