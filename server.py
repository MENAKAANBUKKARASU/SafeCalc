#!/usr/bin/env python3
import os
import sys
import signal
import resource
from asteval import Interpreter

FLAG = os.environ.get("FLAG", "ZCTF2026{fake_flag_run_against_remote}")

BANNER = r"""
  ____        __       ____      _
 / ___| __ _ / _| ___ / ___|__ _| | ___
 \___ \/ _` | |_ / _ \ |   / _` | |/ __|
  ___) | (_| |  _|  __/ |__| (_| | | (__
 |____/ \__,_|_|  \___|\____\__,_|_|\___|

 SafeCalc 1.0 - evaluate math safely with asteval.
 Type a Python expression. 'exit' to quit.
"""

HARD_TIMEOUT = 60
MEM_LIMIT    = 256 * 1024 * 1024


def _limits():
    resource.setrlimit(resource.RLIMIT_AS, (MEM_LIMIT, MEM_LIMIT))
    resource.setrlimit(resource.RLIMIT_CPU, (HARD_TIMEOUT, HARD_TIMEOUT))
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(SystemExit))
    signal.alarm(HARD_TIMEOUT)


def build_interp() -> Interpreter:
    a = Interpreter(err_writer=sys.stderr, no_print=False)
    a.symtable.pop("open", None)

    def version():
        return "SafeCalc 1.0 (asteval)"

    a.symtable["version"] = version
    return a


def main():
    _limits()
    sys.stdout.write(BANNER + "\n")
    sys.stdout.flush()
    a = build_interp()
    while True:
        sys.stdout.write("calc> ")
        sys.stdout.flush()
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if line in ("exit", "quit"):
            break
        if not line:
            continue
        try:
            a.error = []
            out = a(line)
            if a.error:
                for e in a.error:
                    etype, emsg = e.get_error()
                    sys.stdout.write(f"[{etype}] {emsg.splitlines()[-1]}\n")
            elif out is not None:
                sys.stdout.write(repr(out) + "\n")
        except SystemExit:
            break
        except Exception as ex:
            sys.stdout.write(f"[error] {type(ex).__name__}: {ex}\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
