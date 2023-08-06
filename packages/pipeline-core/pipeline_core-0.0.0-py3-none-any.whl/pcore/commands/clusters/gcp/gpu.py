import typing as t
from enum import Enum

from pcore.commands.clusters.enums import GPUType


class _GCPGPUDescription:
    def __init__(
        self, gpu_type: GPUType, instances: t.List[str], accelerator_name: str
    ):
        self.gpu_type = gpu_type
        self.instances = instances
        self.accelerator_name = accelerator_name


class GCPGPU(Enum):
    NVIDIA_T4: _GCPGPUDescription = _GCPGPUDescription(
        GPUType.NVIDIA_T4,
        [
            "n1-highmem-4",
        ],
        "nvidia-tesla-t4",
    )
    NVIDIA_A100: _GCPGPUDescription = _GCPGPUDescription(
        GPUType.NVIDIA_A100,
        [
            "a2-highgpu-1g",
            "a2-highgpu-2g",
            "a2-highgpu-4g",
            "a2-highgpu-8g",
            "a2-megagpu-16g",
        ],
        "nvidia-tesla-a100",
    )
    NVIDIA_A100_80GB: _GCPGPUDescription = _GCPGPUDescription(
        GPUType.NVIDIA_A100_80GB, ["a2-ultragpu-1g"], "nvidia-tesla-a100-80gb"
    )
    NVIDIA_V100: _GCPGPUDescription = _GCPGPUDescription(
        GPUType.NVIDIA_V100,
        [
            "n1-highmem-4",
        ],
        "nvidia-tesla-v100",
    )

    def from_type(gpu_type: GPUType) -> t.Optional["GCPGPU"]:
        for gcp_gpu in GCPGPU:
            if gcp_gpu.value.gpu_type == gpu_type:
                return gcp_gpu
        return None
