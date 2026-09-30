"""
main.py - Entry point for CoinLog
Run: python main.py
"""

def _enable_windows_ansi():
    """Ask the Windows console (cmd or PowerShell) to understand colour codes.
    Returns True if it worked."""
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)          # standard output
        mode = ctypes.c_uint()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        return bool(kernel32.SetConsoleMode(handle, mode.value | 0x0004))
    except Exception:
        return False


def _prepare_console():
    """Make colours and symbols work in PowerShell and cmd, or fall back to plain text."""
    import os
    import sys

    # UTF-8 output so symbols such as the rupee sign never crash printing.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    # Colours only when the terminal can show them. Users can also force plain
    # text themselves by setting the NO_COLOR environment variable.
    if not sys.stdout.isatty():
        os.environ["NO_COLOR"] = "1"
    elif os.name == "nt" and not _enable_windows_ansi():
        os.environ["NO_COLOR"] = "1"


_prepare_console()

from coinlog.cli import run

if __name__ == "__main__":
    run()
