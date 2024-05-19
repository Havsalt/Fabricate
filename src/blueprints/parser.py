r"""

__version__ = "0.1.0"

import argparse


class ParserArguments(argparse.Namespace):
    ... # annotate argument namespace

parser = argparse.ArgumentParser(
    prog="{name}"
)
parser.add_argument("-v", "--version",
                    action="version",
                    version="%(prog)s: v" + __version__)
# add parser arguments here

args = ParserArguments()
parser.parse_args(namespace=args)

# dev
print(args)
"""