from kubernetes import client
from pipeline.console.cloud.gcp.configurations import secrets

__all__ = [
    "compute_resource_cpu_deployment",
]

compute_resource_cpu_deployment = client.V1Deployment(
    api_version="apps/v1",
    kind="Deployment",
    metadata=client.V1ObjectMeta(name="radish-compute-resource-cpu"),
    spec=client.V1DeploymentSpec(
        replicas=3,
        selector=client.V1LabelSelector(
            match_labels={
                "app": "radish-compute-resource-cpu",
            },
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "radish-compute-resource-cpu"},
            ),
            spec=client.V1PodSpec(
                # TODO look at tolerations
                containers=[
                    client.V1Container(
                        name="radish-compute-resource-cpu-container",
                        ports=[
                            client.V1ContainerPort(
                                container_port=80,
                            )
                        ],
                        image="registry.mystic.ai/compute-resource:testing",
                        image_pull_policy="Always",
                        env_from=[
                            secrets._radish_postgres_env_ref,
                            secrets._radish_redis_env_ref,
                            secrets._radish_storage_env_ref,
                        ],
                        env=[
                            client.V1EnvVar(name="APP_NAME", value="compute-resource"),
                            client.V1EnvVar(
                                name="RESOURCE_NAME",
                                value_from=client.V1EnvVarSource(
                                    field_ref=client.V1ObjectFieldSelector(
                                        field_path="metadata.name"
                                    )
                                ),
                            ),
                            client.V1EnvVar(
                                name="RESOURCE_IP",
                                value_from=client.V1EnvVarSource(
                                    field_ref=client.V1ObjectFieldSelector(
                                        field_path="status.podIP"
                                    )
                                ),
                            ),
                        ],
                        liveness_probe=client.V1Probe(
                            _exec=client.V1ExecAction(
                                command=[
                                    "poetry",
                                    "run",
                                    "python",
                                    "/app/docker/alive_check.py",
                                    "||",
                                    "exit 1",
                                ],
                            ),
                            period_seconds=1,
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
# GPU
compute_resource_gpu_deployment = client.V1Deployment(
    api_version="apps/v1",
    kind="Deployment",
    metadata=client.V1ObjectMeta(name="radish-compute-resource-gpu"),
    spec=client.V1DeploymentSpec(
        replicas=3,
        selector=client.V1LabelSelector(
            match_labels={
                "app": "radish-compute-resource-gpu",
            },
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "radish-compute-resource-gpu"},
            ),
            spec=client.V1PodSpec(
                # TODO look at tolerations
                # tolerations=[
                #     client.V1Toleration(
                #         key="nvidia.com/gpu",
                #         operator="Exists",
                #         effect="NoSchedule",
                #     ),
                # ],
                containers=[
                    client.V1Container(
                        name="radish-compute-resource-gpu-container",
                        ports=[
                            client.V1ContainerPort(
                                container_port=80,
                            )
                        ],
                        resources=client.V1ResourceRequirements(
                            limits={"nvidia.com/gpu": 1},
                            requests={"nvidia.com/gpu": 1},
                        ),
                        image="registry.mystic.ai/compute-resource:testing",
                        image_pull_policy="Always",
                        env_from=[
                            secrets._radish_postgres_env_ref,
                            secrets._radish_redis_env_ref,
                            secrets._radish_storage_env_ref,
                        ],
                        env=[
                            client.V1EnvVar(name="APP_NAME", value="compute-resource"),
                            client.V1EnvVar(
                                name="RESOURCE_NAME",
                                value_from=client.V1EnvVarSource(
                                    field_ref=client.V1ObjectFieldSelector(
                                        field_path="metadata.name"
                                    )
                                ),
                            ),
                            client.V1EnvVar(
                                name="RESOURCE_IP",
                                value_from=client.V1EnvVarSource(
                                    field_ref=client.V1ObjectFieldSelector(
                                        field_path="status.podIP"
                                    )
                                ),
                            ),
                            client.V1EnvVar(
                                name="LD_LIBRARY_PATH",
                                value="/usr/local/nvidia/lib:/usr/local/nvidia/lib64",
                            ),
                            client.V1EnvVar(
                                name="PATH",
                                value="$PATH:/usr/local/nvidia/bin:/usr/local/cuda"
                                "/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr"
                                "/bin:/sbin:/bin",
                            ),
                            client.V1EnvVar(
                                name="NVIDIA_VISIBLE_DEVICES",
                                value="all",
                            ),
                            client.V1EnvVar(
                                name="NVIDIA_DRIVER_CAPABILITIES",
                                value="compute,utility",
                            ),
                        ],
                        liveness_probe=client.V1Probe(
                            _exec=client.V1ExecAction(
                                command=[
                                    "poetry",
                                    "run",
                                    "python",
                                    "/app/docker/alive_check.py",
                                    "||",
                                    "exit 1",
                                ],
                            ),
                            period_seconds=1,
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
