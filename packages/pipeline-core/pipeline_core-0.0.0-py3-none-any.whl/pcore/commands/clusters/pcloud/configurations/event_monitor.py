from kubernetes import client
from pipeline.console.cloud.gcp.configurations import secrets

__all__ = [
    "event_monitor_deployment",
]

event_monitor_deployment = client.V1Deployment(
    api_version="apps/v1",
    kind="Deployment",
    metadata=client.V1ObjectMeta(name="radish-event-monitor"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={
                "app": "radish-event-monitor",
            },
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "radish-event-monitor"},
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="radish-event-monitor-container",
                        image="registry.mystic.ai/event-monitor:testing",
                        image_pull_policy="Always",
                        env_from=[
                            secrets._radish_postgres_env_ref,
                            secrets._radish_redis_env_ref,
                            secrets._radish_storage_env_ref,
                        ],
                        env=[
                            client.V1EnvVar(name="PYTHONDONTWRITEBYTECODE", value="1"),
                            client.V1EnvVar(name="PYTHONUNBUFFERED", value="1"),
                        ],
                    )
                ],
                image_pull_secrets=[
                    client.V1LocalObjectReference(name="mystic-registry"),
                ],
            ),
        ),
    ),
)
