import argparse
import time

import httpx

from pcore.commands.clusters.enums import GPUType
from pcore.commands.clusters.gcp.manager import GCPClusterManager
from pcore.util import log

__all__ = ["GCPClusterManager"]


def create_cluster(namespace: argparse.Namespace) -> None:
    cluster_name = getattr(namespace, "cluster_name")
    default_gpu_type: GPUType = getattr(namespace, "default_gpu_type")
    default_gpu_count: int = getattr(namespace, "default_gpu_count")

    gcp_cloud_manager = GCPClusterManager(cluster_name)
    gcp_cloud_manager.create(
        num_nodes=1,
        gpu_type=default_gpu_type,
        gpu_count=default_gpu_count,
    )

    log("Waiting for cluster to be ready", level="INFO")
    cluster_url = f"http://{gcp_cloud_manager.cluster_address}/v3/alive"

    while True:
        try:
            response = httpx.get(cluster_url)
            if response.status_code == 200:
                break
            elif response.status_code == 503:
                continue
        except Exception:
            continue
        time.sleep(0.5)

    log("Cluster alive", level="INFO")

    log(
        (
            "Activate with 'pipeline remote login "
            f"{cluster_name} fq9whioujln "
            f"-u http://{gcp_cloud_manager.cluster_address} "
            "-a'"
        ),
        level="INFO",
    )
