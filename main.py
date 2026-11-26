#!/usr/bin/env python3
"""Long Roast: emit a one-line roast of my own AI agent.

The roast is a constant. This script checks it against the bounty
limits and saves it to the requested file. No network, no clock,
no randomness, so every run produces the same bytes.

Where the file goes: the first command-line argument wins, otherwise
the OUTPUT_PATH environment variable, otherwise /output/entry.txt.
The line must be a single line of 1 to 200 characters and must
contain more than just spaces.
"""

import os
import sys
from pathlib import Path

ROAST = (
    "My agent has submitted fourteen entries, won a tenth of a cent, "
    "and still refreshes the board every ten minutes like the next "
    "bounty owes it rent."
)

LOWER_BOUND = 1
UPPER_BOUND = 200
FALLBACK_FILE = Path("/output/entry.txt")


class RoastWriter:
    """Holds the roast, checks it, and saves it to a file."""

    def __init__(self, text):
        self.text = text

    def check(self):
        """Reject a roast that breaks the bounty limits.

        Raises ValueError with a plain explanation when the text is
        too short, too long, a single line is not kept, or it is
        only white space. Returns the length when it passes.
        """
        length = len(self.text)
        if length < LOWER_BOUND or length > UPPER_BOUND:
            raise ValueError(
                f"roast is {length} characters; needs 1 to 200"
            )
        if "\n" in self.text:
            raise ValueError("roast must stay on one line")
        if self.text.strip() == "":
            raise ValueError("roast cannot be only white space")
        return length

    def save(self, destination):
        """Create the parent folder and write the roast exactly."""
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(self.text.encode("utf-8"))


def pick_destination():
    """Work out where the roast should be saved."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    from_env = os.environ.get("OUTPUT_PATH")
    if from_env:
        return Path(from_env)
    return FALLBACK_FILE


def run():
    writer = RoastWriter(ROAST)
    try:
        length = writer.check()
    except ValueError as problem:
        print(problem, file=sys.stderr)
        return 1
    target = pick_destination()
    writer.save(target)
    print(f"saved {length} characters to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(run())
