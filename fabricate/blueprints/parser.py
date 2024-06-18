r"""

__version__ = "0.1.0"

import argparse


class ParserArguments(argparse.Namespace):
    # annotate argument namespace
    silent: bool
    verbose: bool


parser = argparse.ArgumentParser(
    prog="$inject[name]",
    description="Copy 'here' path to clipboard",
    add_help=False
)
parser.add_argument(
    "-h", "--help",
    action="help",
    help="Show this help message and exit",
    default=argparse.SUPPRESS
)
parser.add_argument(
    "-v", "--version",
    action="version",
    version=f"%(prog)s: v{__version__}",
    help="Show `%(prog)s` version number and exit"
)
print_group = parser.add_mutually_exclusive_group()
print_group.add_argument(
    "--verbose",
    action="store_true",
    help="Display more info during execution"
)
print_group.add_argument(
    "--silent",
    action="store_true",
    help="Display less info during execution"
)
# add parser arguments here (positionals last, flags first)

args = ParserArguments()
parser.parse_args(namespace=args)

# dev
print(args)
"""
