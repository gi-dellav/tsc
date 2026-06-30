"""Entry point for `python -m tsc` and the `tsc` console script."""

import sys

from tsc.app import TSCApp


def main() -> None:
    args = sys.argv[1:]
    history = None
    if args:
        history = args[0]
    app = TSCApp(history_filename=history)
    app.run()


if __name__ == "__main__":
    main()
