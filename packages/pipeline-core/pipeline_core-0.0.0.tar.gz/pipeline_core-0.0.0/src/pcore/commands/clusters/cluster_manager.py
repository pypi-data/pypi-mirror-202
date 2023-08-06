import re

from kubernetes import client, utils

from pcore.commands.clusters.enums import CloudProvider


class ClusterManager:
    def __init__(
        self,
        cluster_name: str,
        *,
        cloud_provider: CloudProvider,
    ):
        self.cloud_provider = cloud_provider
        self.cluster_name = cluster_name
        self.cluster_address: str = None

        self.kube_coreV1_client: client.CoreV1Api = None
        self.kube_api_client: client.ApiClient = None
        self.kube_networking_api: client.NetworkingV1Api = None

    def rollback(self):
        raise NotImplementedError()

    def create(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def apply_k8s_config(
        self,
        config_dict: dict,
    ):
        under_pat = re.compile(r"_([a-z])")

        def remove_start_underscore(x):
            return x[1:] if str(x)[0] == "_" else x

        def underscore_to_camel(name):
            name = remove_start_underscore(name)
            return under_pat.sub(lambda x: x.group(1).upper(), name)

        def convert_dict_keys_to_camel(d):
            result = {}
            for k, v in d.items():
                if v is None:
                    continue

                if isinstance(v, list):
                    result[underscore_to_camel(k)] = [
                        convert_dict_keys_to_camel(item)
                        if isinstance(item, dict)
                        else item
                        for item in v
                    ]
                    continue

                result[underscore_to_camel(k)] = (
                    convert_dict_keys_to_camel(v) if isinstance(v, dict) else v
                )

            return result

        formatted_dict = convert_dict_keys_to_camel(config_dict)
        utils.create_from_dict(
            k8s_client=self.kube_api_client,
            data=formatted_dict,
            namespace=self.cluster_name,
        )

    @staticmethod
    def load_kubeconfig() -> None:
        raise NotImplementedError()

    def create_k8s_clients(self) -> None:
        self.kube_coreV1_client = client.CoreV1Api()
        self.kube_api_client = client.ApiClient()
        self.kube_networking_api = client.NetworkingV1Api()
