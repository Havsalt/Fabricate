
__version__ = "0.1.0"

import argparse
import pathlib

import pyperclip as clipboard

from scanning import collect_format_keys


class ParserArguments(argparse.Namespace):
    blueprint: str
    verbose: bool
    quiet: bool
    arguments: list[str]


parser = argparse.ArgumentParser(
    prog="Fabricate",
)

subparsers = parser.add_subparsers(required=True, dest="blueprint")

# generate flags
path_generator = (
    pathlib.Path(__file__)
    .parent
    .joinpath("blueprints")
    .iterdir()
)
for path in path_generator:
    if not path.stem.startswith("__"):
        command = path.stem
        subparser = subparsers.add_parser(command)
        subparser.add_argument("arguments", nargs="*")
        print_group = subparser.add_mutually_exclusive_group()
        print_group.add_argument("-v", "--verbose", action="store_true", help="Verbose")
        print_group.add_argument("-q", "--quiet", action="store_true", help="Quiet")
        template = (
            pathlib.Path(__file__)
            .parent
            .joinpath("blueprints", path.name)
            .read_text(encoding="utf-8")
        )
        pre_formatted: str = eval(template).removeprefix("\n")
        for key in collect_format_keys(pre_formatted):
            subparser.add_argument(f"--{key}", required=True)

# parse arguments into a typed namespace
args = ParserArguments()
parser.parse_args(namespace=args)

keys: dict[str, str] = {
    key: value
    for key, value in args.__dict__.items()
    if key not in args.__annotations__
}

template = (
    pathlib.Path(__file__)
    .parent
    .joinpath("blueprints", args.blueprint)
    .with_suffix(".py")
    .read_text(encoding="utf-8")
    .format(*args.arguments, **keys)
)
rendered: str = eval(template).removeprefix("\n")

clipboard.copy(rendered)

if args.verbose:
    line_count = rendered.count('\n')
    print(f"[Info] Fabricated blueprint '{args.blueprint}' ({line_count} lines):")
if not args.quiet:
    print(rendered)
