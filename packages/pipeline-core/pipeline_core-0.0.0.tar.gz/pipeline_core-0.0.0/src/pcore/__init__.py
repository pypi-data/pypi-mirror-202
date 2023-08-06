import argparse
import sys
import traceback
import typing as t

from pcore.commands.clusters import create_parser as create_clusters_parser
from pcore.commands.credentials import create_parser as create_credentials_parser


def construct_cli() -> argparse.ArgumentParser:
    base_parser = argparse.ArgumentParser(
        prog="pcore",
        description="A CLI for PipelineCore.",
        add_help=True,
    )

    base_parser.add_argument(
        "-v",
        "--verbose",
        help="Enable verbose logging.",
        action="store_true",
    )

    command_parsers = base_parser.add_subparsers(
        dest="command",
    )

    create_credentials_parser(command_parsers)
    create_clusters_parser(command_parsers)

    return base_parser


def execute_cli(
    parser: argparse.ArgumentParser,
    args: t.Optional[t.List[str]] = None,
) -> None:
    if args is None:
        args = sys.argv[1:]

    parsed_args = parser.parse_args(args=args)

    if (selected_func := getattr(parsed_args, "func", None)) is not None:
        selected_func(parsed_args)

    if parsed_args.command is None:
        parser.print_help()
        return


def cli_entry() -> None:
    try:
        parser = construct_cli()
        execute_cli(parser)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
