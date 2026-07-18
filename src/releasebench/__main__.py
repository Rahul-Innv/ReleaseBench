"""Module entry point: route one JSON request from stdin or a file argument."""

from releasebench.router import main

if __name__ == "__main__":
    raise SystemExit(main())
