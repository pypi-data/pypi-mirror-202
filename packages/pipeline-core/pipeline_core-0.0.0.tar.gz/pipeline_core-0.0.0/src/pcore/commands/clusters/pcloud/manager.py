import base64
import os
import random
import string
import time

from kubernetes import client
from kubernetes.client.rest import ApiException

from pcore.commands.clusters import ClusterManager
from pcore.commands.clusters.enums import CloudProvider
from pcore.commands.clusters.pcloud import configurations as pcloud_configurations
from pcore.util import ProgressContext, log


class PCloudClusterManager(ClusterManager):
    def __init__(
        self,
        cluster_name: str,
        *,
        cloud_provider: CloudProvider = CloudProvider.PCLOUD,
    ):
        super().__init__(cluster_name=cluster_name, cloud_provider=cloud_provider)
        self.storage_bucket_name = f"radish-{cluster_name}"
        self.storage_sk = "..."
        self.storage_ak = "compute-engine-testing"
        self.storage_url = "https://storage.services.mystic.ai"

    def create(self):
        with ProgressContext():
            try:
                ProgressContext.set_text("Creating kubernetes clients")
                self.create_k8s_clients()

                ProgressContext.set_text("Creating namespace")
                self._kube_create_namespace()
                ProgressContext.set_text("Adding registry secrets")
                self._kube_add_registry_secrets()
                ProgressContext.set_text("Creating environment variables")
                self._kube_create_env_variables()
                ProgressContext.set_text("Creating postgres service")
                self._kube_create_postgres()
                ProgressContext.set_text("Creating redis service")
                self._kube_create_redis()
                ProgressContext.set_text("Setting up Radish")
                self._kube_create_radish_services()
                ProgressContext.set_text("Creating Radish ingress")
                self._kube_create_ingress()

            except ApiException as e:
                log(e.message, "ERROR")
                log("Failed to create radish services, rolling back...", "ERROR")
                self.rollback()

    def delete(self):
        raise NotImplementedError()

    def rollback(self):
        raise NotImplementedError()

    def _kube_create_namespace(self) -> None:
        body = client.V1Namespace(metadata=client.V1ObjectMeta(name=self.cluster_name))
        self.kube_coreV1_client.create_namespace(body)

    def _kube_add_registry_secrets(self) -> None:
        with open(os.path.expanduser("~/.docker/config.json"), "r") as config_file:
            config_file_data = config_file.read()

        secret_body = client.V1Secret(
            metadata=client.V1ObjectMeta(
                name="mystic-registry", namespace=self.cluster_name
            ),
            data={
                ".dockerconfigjson": base64.b64encode(
                    config_file_data.encode()
                ).decode()
            },
            type="kubernetes.io/dockerconfigjson",
        )

        self.kube_coreV1_client.create_namespaced_secret(
            namespace=self.cluster_name, body=secret_body
        )

    def _kube_create_env_variables(self) -> None:
        postgres_vars = {
            "POSTGRES_DRIVER": "psycopg2",
            "POSTGRES_USER": str(_random_string(20)),
            "POSTGRES_PASSWORD": str(_random_string(20)),
            "POSTGRES_HOST": f"radish-postgres-svc.{self.cluster_name}"
            ".svc.cluster.local",
            "POSTGRES_PORT": "5432",
            "POSTGRES_DB": "radish",
        }

        postgres_body = client.V1Secret(
            metadata=client.V1ObjectMeta(
                name="radish-postgres-env", namespace=self.cluster_name
            ),
            data={
                key: base64.b64encode(value.encode()).decode()
                for key, value in postgres_vars.items()
            },
        )

        self.kube_coreV1_client.create_namespaced_secret(
            body=postgres_body, namespace=self.cluster_name
        )

        # Redis
        redis_vars = {
            "REDIS_HOST": f"radish-redis-svc.{self.cluster_name}.svc.cluster.local",
        }

        redis_body = client.V1Secret(
            metadata=client.V1ObjectMeta(
                name="radish-redis-env", namespace=self.cluster_name
            ),
            data={
                key: base64.b64encode(value.encode()).decode()
                for key, value in redis_vars.items()
            },
        )

        self.kube_coreV1_client.create_namespaced_secret(
            body=redis_body, namespace=self.cluster_name
        )

        # Storage
        storage_vars = {
            "AWS_ACCESS_KEY_ID": self.storage_ak,
            "AWS_SECRET_ACCESS_KEY": self.storage_sk,
            "S3_BUCKET_NAME": self.storage_bucket_name,
            "MINIO_URL": self.storage_url,
        }
        storage_body = client.V1Secret(
            metadata=client.V1ObjectMeta(
                name="radish-storage-env", namespace=self.cluster_name
            ),
            data={
                key: base64.b64encode(value.encode()).decode()
                for key, value in storage_vars.items()
            },
        )

        self.kube_coreV1_client.create_namespaced_secret(
            body=storage_body, namespace=self.cluster_name
        )

    def _kube_create_postgres(self) -> None:
        self.apply_k8s_config(pcloud_configurations.postgres_pv.to_dict())
        self.apply_k8s_config(pcloud_configurations.postgres_pvc.to_dict())
        self.apply_k8s_config(pcloud_configurations.postgres_deployment.to_dict())
        self.apply_k8s_config(pcloud_configurations.postgres_service.to_dict())

    def _kube_create_redis(self) -> None:
        self.apply_k8s_config(pcloud_configurations.redis_deployment.to_dict())
        self.apply_k8s_config(pcloud_configurations.redis_svc.to_dict())

    def _kube_create_radish_services(self) -> None:
        deployment_array = [
            pcloud_configurations.event_monitor_deployment,
            pcloud_configurations.main_api_deployment,
            pcloud_configurations.main_api_service,
            pcloud_configurations.compute_resource_gpu_deployment,
        ]

        for deployment in deployment_array:
            time.sleep(1.0)
            self.apply_k8s_config(deployment)

    def _kube_create_ingress(self) -> None:
        self.kube_networking_api.create_namespaced_ingress(
            namespace=self.cluster_name,
            body=pcloud_configurations.main_api_ingress(self.cluster_name),
        )


def _random_string(k: int) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=k))
