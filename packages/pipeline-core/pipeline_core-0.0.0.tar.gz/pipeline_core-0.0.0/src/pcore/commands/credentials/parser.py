import argparse

from pcore.commands.credentials.gcp import add_credentials as add_gcp_credentials

command_aliases = ["credential", "credentials", "creds", "cred"]


def create_parser(
    command_parser: "argparse._SubParsersAction[argparse.ArgumentParser]",
) -> None:
    credendial_parser = command_parser.add_parser(
        "credentials",
        aliases=command_aliases,
        description="Manage cloud credentials.",
        help="Manage cloud credentials.",
    )
    credendial_parser.set_defaults(func=lambda _: credendial_parser.print_help())

    credential_sub_parser = credendial_parser.add_subparsers(
        dest="sub-command",
    )

    _create_add_parser(credential_sub_parser)


def _create_add_parser(
    credential_sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]",
) -> None:
    add_sub_parser = credential_sub_parser.add_parser(
        *["add"],
        description="Add a new credential for cloud provider.",
        help="Add a new credential for cloud provider.",
    )
    add_sub_parser.set_defaults(func=lambda _: add_sub_parser.print_help())

    cloud_sub_parser = add_sub_parser.add_subparsers(
        dest="cloud-provider",
    )

    gcp_auth_parser = cloud_sub_parser.add_parser(
        "gcp",
        description="Add a new GCP credential.",
        help="Add a new GCP credential.",
    )
    gcp_auth_parser.set_defaults(func=add_gcp_credentials)

    gcp_auth_parser.add_argument(
        "--service-account-path",
        help="Path to the service account JSON file.",
        required=False,
        default=None,
    )
    gcp_auth_parser.add_argument(
        "project_id",
        help="The GCP project ID.",
    )
