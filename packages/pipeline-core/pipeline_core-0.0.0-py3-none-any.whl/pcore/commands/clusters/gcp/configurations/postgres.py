from kubernetes import client
from pipeline.console.cloud.gcp.configurations import secrets

__all__ = ["postgres_deployment", "postgres_pvc", "postgres_service"]

postgres_deployment = client.V1Deployment(
    api_version="apps/v1",
    kind="Deployment",
    metadata=client.V1ObjectMeta(name="radish-postgres"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={
                "app": "radish-postgres",
            },
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "radish-postgres"},
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="radish-postgres",
                        ports=[
                            client.V1ContainerPort(
                                container_port=5432,
                            ),
                        ],
                        image="postgres",
                        image_pull_policy="Always",
                        env_from=[
                            secrets._radish_postgres_env_ref,
                        ],
                        volume_mounts=[
                            client.V1VolumeMount(
                                mount_path="/var/lib/postgresql/data",
                                name="radish-postgres-data",
                                sub_path="radish-postgres-data",
                            )
                        ],
                    )
                ],
                volumes=[
                    client.V1Volume(
                        name="radish-postgres-data",
                        persistent_volume_claim=(
                            client.V1PersistentVolumeClaimVolumeSource(
                                claim_name="radish-postgres-pvc",
                            )
                        ),
                    )
                ],
            ),
        ),
    ),
)

postgres_pvc = client.V1PersistentVolumeClaim(
    api_version="v1",
    kind="PersistentVolumeClaim",
    metadata=client.V1ObjectMeta(name="radish-postgres-pvc"),
    spec=client.V1PersistentVolumeClaimSpec(
        access_modes=["ReadWriteOnce"],
        storage_class_name="standard-rwo",
        resources=client.V1ResourceRequirements(
            requests={"storage": "8Gi"},
        ),
    ),
)

# postgres_pv = client.V1PersistentVolume(
#     api_version="v1",
#     kind="PersistentVolume",
#     metadata=client.V1ObjectMeta(
#         name="radish-postgres-pv",
#         labels={
#             "app": "radish-postgres",
#         },
#     ),
#     spec=client.V1PersistentVolumeSpec(
#         storage_class_name="standard-rwo",
#         capacity={"storage": "32Gi"},
#         access_modes=["ReadWriteMany"],
#         gce_persistent_disk=
#     )
# )

postgres_service = client.V1Service(
    api_version="v1",
    kind="Service",
    metadata=client.V1ObjectMeta(name="radish-postgres-svc"),
    spec=client.V1ServiceSpec(
        type="NodePort",
        selector={"app": "radish-postgres"},
        ports=[
            client.V1ServicePort(
                port=5432,
                target_port=5432,
            )
        ],
    ),
)
