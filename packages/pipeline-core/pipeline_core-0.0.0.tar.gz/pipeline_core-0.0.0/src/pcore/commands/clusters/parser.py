import argparse

from pcore.commands.clusters.enums import GPUType
from pcore.commands.clusters.gcp import create_cluster as create_gcp_cluster

command_aliases = ["cluster", "clusters"]


def create_parser(
    command_parser: "argparse._SubParsersAction[argparse.ArgumentParser]",
) -> None:
    cluster_parser = command_parser.add_parser(
        "cluster",
        aliases=command_aliases,
        description="Manage radish clusters.",
        help="Manage radish clusters.",
    )
    cluster_parser.set_defaults(func=lambda _: cluster_parser.print_help())

    cluster_sub_parser = cluster_parser.add_subparsers(
        dest="sub-command",
    )

    _create_add_parser(cluster_sub_parser)


def _create_add_parser(
    cluster_sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]",
) -> None:
    add_sub_parser = cluster_sub_parser.add_parser(
        "add",
        aliases=["create"],
        description="Add a new cluster for cloud provider.",
        help="Add a new cluster for cloud provider.",
    )
    add_sub_parser.set_defaults(func=lambda _: add_sub_parser.print_help())

    cloud_sub_parser = add_sub_parser.add_subparsers(
        dest="cloud-provider",
    )

    gcp_add_parser = cloud_sub_parser.add_parser(
        "gcp",
        description="Create a new GCP cluster.",
        help="Create a new GCP cluster.",
    )
    gcp_add_parser.set_defaults(func=create_gcp_cluster)

    gcp_add_parser.add_argument(
        "--cluster-name",
        "-n",
        help="Name of the cluster.",
        default="radish-cluster",
    )

    gcp_add_parser.add_argument(
        "--default-gpu-type",
        help="Default GPU type to use for the cluster.",
        type=GPUType,
        choices=list(GPUType),
        default=GPUType.NVIDIA_T4,
    )

    gcp_add_parser.add_argument(
        "--default-gpu-count",
        help="Default GPU count to use for the cluster.",
        type=int,
        default=3,
    )
