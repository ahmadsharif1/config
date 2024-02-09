import argparse
import os
import signal
import sys
import threading
import pywatchman
import subprocess
from my_runner import MyRunner


# Copied over from pywatchman.
def patterns_to_terms(pats):
    # convert a list of globs into the equivalent watchman expression term
    if pats is None or len(pats) == 0:
        return ["true"]
    terms = ["anyof"]
    for p in pats:
        terms.append(["match", p, "wholename", {"includedotfiles": True}])
    return terms


def Main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--patterns",
        type=str,
        nargs="+",
        default=["**/*.cpp", "**/*.h", "**/*.py", "**/TARGETS"],
        help="Patterns to match",
    )
    parser.add_argument("--root", type=str, default=".", help="Root directory to watch")
    client = pywatchman.client(timeout=60 * 60 * 24)
    client.capabilityCheck(required=["cmd-watch-project", "wildmatch"])
    args, unknown_args = parser.parse_known_args()
    root_dir = os.path.abspath(os.path.expanduser(args.root))

    query = {"expression": patterns_to_terms(args.patterns), "fields": ["name"]}
    query["since"] = client.query("clock", root_dir)["clock"]
    sub = client.query("subscribe", root_dir, "ahmads_persist", query)
    runner = MyRunner(unknown_args)
    # Run once at the beginning.
    runner.on_change(None)
    while True:
        try:
            result = client.receive()
            #print("Received result: ", result)
            runner.on_change(None)
        except KeyboardInterrupt:
            print("User pressed Ctrl-C, exiting...")
            break
    return 0


if __name__ == "__main__":
    Main(sys.argv)
