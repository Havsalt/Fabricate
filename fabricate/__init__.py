
__version__ = "0.4.0"

import argparse
import pathlib

import pyperclip as clipboard
from actus import info

from .substition import collect_format_keys, inject_values


class ParserArguments(argparse.Namespace):
    blueprint: str
    verbose: bool
    silent: bool
    arguments: list[str]


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="fab",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s: v" + __version__
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
            print_group.add_argument("--verbose", action="store_true", help="Verbose")
            print_group.add_argument("--silent", action="store_true", help="Silent")
            template = (
                pathlib.Path(__file__)
                .parent
                .joinpath("blueprints", path.name)
                .read_text(encoding="utf-8")
            )
            pre_formatted: str = eval(template).removeprefix("\n")
            unique_keys = set(collect_format_keys(pre_formatted))
            for key in unique_keys:
                subparser.add_argument(f"--{key}", required=True)

    # parse arguments into a typed namespace
    args = ParserArguments()
    parser.parse_args(namespace=args)

    args_keys: dict[str, str] = {
        key: value
        for key, value in args.__dict__.items()
        if key not in args.__annotations__
    }

    raw_template = (
        pathlib.Path(__file__)
        .parent
        .joinpath("blueprints", args.blueprint.lower())
        .with_suffix(".py")
        .read_text(encoding="utf-8")
    )
    keywords = set(collect_format_keys(raw_template))
    pairs = {
        keyword: args_keys[keyword]
        for keyword in keywords
    }
    template = inject_values(raw_template, pairs=pairs, blueprint_name=args.blueprint.lower())
    rendered: str = eval(template).removeprefix("\n")

    clipboard.copy(rendered)

    if args.verbose:
        line_count = rendered.count('\n')
        info(f"Fabricated blueprint $[{args.blueprint}] (Linecount: $[{line_count}])")
    if not args.silent:
        print(rendered)
    
    return 0
