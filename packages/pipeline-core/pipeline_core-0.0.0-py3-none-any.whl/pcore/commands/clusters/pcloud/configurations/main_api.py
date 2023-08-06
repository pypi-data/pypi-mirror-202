from kubernetes import client

from pcore.commands.clusters.pcloud.configurations import secrets

main_api_deployment = client.V1Deployment(
    api_version="apps/v1",
    kind="Deployment",
    metadata=client.V1ObjectMeta(name="radish-main-api"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={
                "app": "radish-main-api",
            },
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "radish-main-api"},
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="radish-main-api",
                        ports=[
                            client.V1ContainerPort(
                                container_port=80,
                                name="http",
                            )
                        ],
                        image="registry.mystic.ai/compute-engine-api:testing",
                        image_pull_policy="Always",
                        env_from=[
                            secrets._radish_postgres_env_ref,
                            secrets._radish_redis_env_ref,
                            secrets._radish_storage_env_ref,
                        ],
                        env=[
                            client.V1EnvVar(name="POSTGRES_DRIVER", value="asyncpg"),
                            client.V1EnvVar(name="ROOT_TOKEN", value="fq9whioujln"),
                        ],
                        liveness_probe=client.V1Probe(
                            http_get=client.V1HTTPGetAction(
                                path="/v3/alive",
                                scheme="HTTP",
                                port=80,
                            ),
                        ),
                        readiness_probe=client.V1Probe(
                            http_get=client.V1HTTPGetAction(
                                path="/v3/alive",
                                scheme="HTTP",
                                port=80,
                            ),
                        ),
                    )
                ],
                image_pull_secrets=[
                    client.V1LocalObjectReference(name="mystic-registry"),
                ],
            ),
        ),
    ),
)

main_api_service = client.V1Service(
    api_version="v1",
    kind="Service",
    metadata=client.V1ObjectMeta(name="radish-main-api-svc"),
    spec=client.V1ServiceSpec(
        type="NodePort",
        selector={"app": "radish-main-api"},
        ports=[
            client.V1ServicePort(
                port=80,
                target_port=80,
            )
        ],
    ),
)


def main_api_ingress(namespace: str) -> client.V1Ingress:
    """
    Creates an ingress for the main API.

    Args:
        namespace (str): The namespace to create the ingress in.

    Returns:
        client.V1Ingress: The ingress object.
    """
    return client.V1Ingress(
        api_version="networking.k8s.io/v1",
        kind="Ingress",
        metadata=client.V1ObjectMeta(name="radish-main-api-ingress"),
        spec=client.V1IngressSpec(
            ingress_class_name="nginx-ingress-controller",
            rules=[
                client.V1IngressRule(
                    host=f"{namespace}.cluster.pipeline.ai",
                    http=client.V1HTTPIngressRuleValue(
                        paths=[
                            client.V1HTTPIngressPath(
                                path="/",
                                path_type="Prefix",
                                backend=client.V1IngressBackend(
                                    service=client.V1IngressServiceBackend(
                                        name="radish-main-api-svc",
                                        port=client.V1ServiceBackendPort(
                                            number=80,
                                        ),
                                    )
                                ),
                            )
                        ]
                    ),
                )
            ],
        ),
    )
