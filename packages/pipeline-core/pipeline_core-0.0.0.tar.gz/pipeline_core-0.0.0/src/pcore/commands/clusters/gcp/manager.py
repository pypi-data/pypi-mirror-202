import os
import subprocess
import traceback
import typing as t

import backoff
import httpx
import yaml
from google.api_core.exceptions import PermissionDenied
from google.cloud import compute_v1, container_v1, storage
from google.oauth2 import service_account
from kubernetes import config
from pipeline.configuration import current_configuration

from pcore.commands.clusters import CloudProvider, GPUType
from pcore.commands.clusters.gcp import configurations as gcp_configurations
from pcore.commands.clusters.gcp import gpu as gcp_gpu
from pcore.commands.clusters.pcloud import PCloudClusterManager
from pcore.util import ProgressContext, log


class GCPClusterManager(PCloudClusterManager):
    def __init__(
        self,
        cluster_name: str,
        *,
        project_id: str = current_configuration.get_google_auth_project_id(),
        location: str = "europe-west4",
    ):
        super().__init__(
            cluster_name=cluster_name,
            cloud_provider=CloudProvider.GCP,
        )
        self.credentials = service_account.Credentials.from_service_account_info(
            current_configuration.get_google_auth_service_account(),
        )

        self.gcp_gke_client = container_v1.ClusterManagerClient(
            credentials=self.credentials
        )

        self.gcp_addresses_client = compute_v1.GlobalAddressesClient(
            credentials=self.credentials,
        )

        self.gcp_storage_client = storage.Client(
            credentials=self.credentials,
        )

        self.project_id = project_id
        self.location = location

        self.storage_ak: str = None
        self.storage_sk: str = None

    def create(
        self,
        num_nodes: int = 1,
        machine_type: str = "",
        gpu_type: GPUType = GPUType.NVIDIA_T4,
        gpu_count: int = 3,
    ):
        log("Creating a new Radish cluster on GCP (this may take up to 10mins)")

        with ProgressContext():
            ProgressContext.set_text("Creating GKE cluster...")
            self._create_gke_cluster(
                num_nodes=num_nodes,
                machine_type=machine_type,
            )
        log(f"GKE cluster created with name {self.cluster_name}", "SUCCESS")

        log("Getting GKE cluster credentials")
        self._update_k8s_config()

        log("Creating external static IP address")
        self._create_gke_static_ip()

        log("Setting up storage")
        self._create_storage_credentials()

        super().create()
        # log("Installing Nvidia drivers")
        # nvidia_
        log("Creating GPU cluster (T4)")
        self._create_gke_gpu_node_pool(gpu_type=gpu_type, gpu_count=gpu_count)

        log("Radish cluster created successfully", "SUCCESS")

    def delete(self):
        with ProgressContext():
            try:
                ProgressContext.set_text("Deleting GCP static IP address")
                self._delete_gke_static_ip()
            except Exception:
                traceback.print_exc()
                log("Failed to delete static IP address", "ERROR")

            try:
                ProgressContext.set_text("Deleting GKE cluster")
                cluster_location = self.gcp_gke_client.common_location_path(
                    self.project_id, self.location
                )
                cluster_name = f"{cluster_location}/clusters/{self.cluster_name}"

                request = {"name": cluster_name}
                self.gcp_gke_client.delete_cluster(request)

                ProgressContext.set_text("Deleting GKE cluster")
            except PermissionDenied:
                log("You do not have permission to delete this cluster", "ERROR")

    def rollback(self):
        self.delete()

    def _kube_create_postgres(self) -> None:
        self.apply_k8s_config(gcp_configurations.postgres_pvc.to_dict())
        self.apply_k8s_config(gcp_configurations.postgres_deployment.to_dict())
        self.apply_k8s_config(gcp_configurations.postgres_service.to_dict())

    @staticmethod
    def load_kubeconfig() -> None:
        config_data = current_configuration.get_google_kubeconfig()
        config.load_kube_config_from_dict(config_data)

    def _update_k8s_config(self) -> None:
        path = "~/.kube/config"
        abspath = os.path.expanduser(path)
        if not os.path.exists(abspath):
            raise Exception(f"Kubernetes configuration file does not exist: {abspath}")

        with open(abspath, "r") as config_file:
            raw_yaml = yaml.safe_load(config_file)

        current_configuration.set_gcp_kubeconfig(raw_yaml)
        self.load_kubeconfig()

    def _create_gke_cluster(self, num_nodes: int, machine_type: str):
        cluster_location = self.gcp_gke_client.common_location_path(
            self.project_id, self.location
        )
        cluster_def = {
            "name": self.cluster_name,
            "initial_node_count": num_nodes,
            "node_config": {"machine_type": machine_type},
            "resource_labels": {"radish": "sprout"},
        }
        request = {"parent": cluster_location, "cluster": cluster_def}
        try:
            create_response = self.gcp_gke_client.create_cluster(request)
        except PermissionDenied as e:
            log(e.message, "ERROR")

        op_identifier = f"{cluster_location}/operations/{create_response.name}"
        _poll_for_op_status(self.gcp_gke_client, op_identifier, "Create GKE cluster")

        output = subprocess.run(
            [
                "gcloud",
                "container",
                "clusters",
                "get-credentials",
                self.cluster_name,
                "--region",
                self.location,
                "--project",
                self.project_id,
            ]
        )
        if output.returncode != 0:
            raise Exception("Failed to get credentials for GKE cluster")

    def _create_gke_gpu_node_pool(
        self,
        gpu_type: GPUType = GPUType.NVIDIA_T4,
        gpu_count: int = 3,
    ) -> None:
        gcp_gpu_type = gcp_gpu.GCPGPU.from_type(gpu_type)

        cluster_location = self.gcp_gke_client.common_location_path(
            self.project_id, self.location
        )

        create_response = self.gcp_gke_client.create_node_pool(
            project_id=self.project_id,
            parent=cluster_location,
            cluster_id=self.cluster_name,
            node_pool=container_v1.NodePool(
                name="gpu-pool",
                initial_node_count=gpu_count,
                locations=["europe-west4-a"],
                config=container_v1.NodeConfig(
                    machine_type=gcp_gpu_type.value.instances[0],
                    accelerators=[
                        container_v1.AcceleratorConfig(
                            accelerator_count=1,
                            accelerator_type=gcp_gpu_type.value.accelerator_name,
                        )
                    ],
                ),
            ),
        )

        op_identifier = f"{cluster_location}/operations/{create_response.name}"
        _poll_for_op_status(self.gcp_gke_client, op_identifier, "Create GPU pool")

        nvidia_daemon_raw = httpx.get(
            "https://raw.githubusercontent.com/GoogleCloudPlatform/"
            "container-engine-accelerators/master/nvidia-driver-inst"
            "aller/cos/daemonset-preloaded-latest.yaml"
        )

        nvidia_daemon_config = yaml.safe_load(nvidia_daemon_raw.text)

        self.apply_k8s_config(nvidia_daemon_config)

    def _create_gke_static_ip(self) -> None:
        output = self.gcp_addresses_client.insert(
            project=self.project_id,
            address_resource=compute_v1.Address(
                name=self.cluster_name,
            ),
        )

        output.result()

        new_address = self.gcp_addresses_client.get(
            address=self.cluster_name, project=self.project_id
        )

        self.cluster_address = new_address.address

    def _delete_gke_static_ip(self) -> None:
        self.gcp_addresses_client.delete(
            project=self.project_id,
            address=self.cluster_name,
        )

    def _create_storage_credentials(self) -> None:
        hmac_key, secret = self.gcp_storage_client.create_hmac_key(
            service_account_email=self.credentials.service_account_email,
            project_id=self.project_id,
        )

        self.storage_ak = hmac_key.access_id
        self.storage_sk = secret
        self.storage_url = "https://storage.googleapis.com"
        try:
            self.gcp_storage_client.create_bucket(
                self.storage_bucket_name,
                location="europe-west4",
            )
        except Exception:
            traceback.print_exc()

    def _delete_storage_credentials(self) -> None:
        self.gcp_storage_client.bucket(self.storage_bucket_name).delete(force=True)

    def _kube_create_ingress(self) -> None:
        body = gcp_configurations.main_api_ingress(self.cluster_name)

        self.kube_networking_api.create_namespaced_ingress(
            namespace=self.cluster_name,
            body=body,
        )

    def _kube_create_radish_services(self) -> None:
        deployment_array = [
            gcp_configurations.event_monitor_deployment.to_dict(),
            gcp_configurations.main_api_deployment.to_dict(),
            gcp_configurations.main_api_service.to_dict(),
            gcp_configurations.compute_resource_gpu_deployment.to_dict(),
        ]

        for deployment in deployment_array:
            self.apply_k8s_config(deployment)


def _on_success(details: t.Dict[str, str]) -> None:
    ProgressContext.set_text(
        "Successfully created cluster after {elapsed:0.1f} seconds".format(**details)
    )


def _on_failure(details: t.Dict[str, str]) -> None:
    ...


@backoff.on_predicate(
    backoff.constant,
    lambda x: x != container_v1.Operation.Status.DONE,
    on_backoff=_on_failure,
    on_success=_on_success,
    interval=2.0,
)
def _poll_for_op_status(
    client: container_v1.ClusterManagerClient, op_id: str, operation_name: str = ""
) -> container_v1.Operation.Status:
    op = client.get_operation({"name": op_id})

    all_metrics = op.progress.metrics

    metric_values = {
        m.name: m.int_value for m in all_metrics if not m.name.endswith("TOTAL")
    }

    metric_totals = {
        m.name: m.int_value for m in all_metrics if m.name.endswith("TOTAL")
    }

    metric_progress = {
        metric_name: metric_value / metric_totals[metric_name + "_TOTAL"]
        for metric_name, metric_value in metric_values.items()
    }
    if len(metric_progress) > 0:
        last_item = list(metric_progress.items())[-1]
        percentage_string = "{:.0%}".format(last_item[1])
        ProgressContext.set_text(
            "Current GKE cluster status: " f"{last_item[0]}={percentage_string}"
        )
    else:
        ProgressContext.set_text("Current GKE cluster status: Waiting...")

    return op.status


__all__ = ["GCPClusterManager"]
