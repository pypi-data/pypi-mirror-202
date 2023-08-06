from enum import Enum


class CloudProvider(Enum):
    PCLOUD: str = "pcloud"
    GCP: str = "gcp"


class GPUType(Enum):
    NVIDIA_T4: str = "nvidia-tesla-t4"
    NVIDIA_V100: str = "nvidia-tesla-v100"
    NVIDIA_A100: str = "nvidia-tesla-a100"
    NVIDIA_A100_80GB: str = "nvidia-tesla-a100-80gb"
