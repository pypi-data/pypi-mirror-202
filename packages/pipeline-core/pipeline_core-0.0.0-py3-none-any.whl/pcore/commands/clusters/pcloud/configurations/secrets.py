from kubernetes import client

_radish_postgres_env_ref = client.V1EnvFromSource(
    secret_ref=client.V1SecretReference(
        name="radish-postgres-env",
    )
)
_radish_redis_env_ref = client.V1EnvFromSource(
    secret_ref=client.V1SecretReference(
        name="radish-redis-env",
    )
)
_radish_storage_env_ref = client.V1EnvFromSource(
    secret_ref=client.V1SecretReference(
        name="radish-storage-env",
    )
)
