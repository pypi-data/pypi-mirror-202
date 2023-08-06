from kubernetes import client
from pipeline.console.cloud.gcp.configurations import secrets

__all__ = ["redis_deployment", "redis_svc"]

redis_deployment = client.V1Deployment(
    api_version="apps/v1",
    kind="Deployment",
    metadata=client.V1ObjectMeta(name="radish-redis"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={
                "app": "radish-redis",
            },
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "radish-redis"},
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="radish-redis",
                        ports=[
                            client.V1ContainerPort(
                                container_port=6379,
                            )
                        ],
                        image="redis",
                        image_pull_policy="Always",
                        env_from=[
                            secrets._radish_redis_env_ref,
                        ],
                    )
                ],
            ),
        ),
    ),
)

redis_svc = client.V1Service(
    api_version="v1",
    kind="Service",
    metadata=client.V1ObjectMeta(name="radish-redis-svc"),
    spec=client.V1ServiceSpec(
        selector={"app": "radish-redis"},
        ports=[
            client.V1ServicePort(
                port=6379,
                target_port=6379,
            )
        ],
    ),
)
