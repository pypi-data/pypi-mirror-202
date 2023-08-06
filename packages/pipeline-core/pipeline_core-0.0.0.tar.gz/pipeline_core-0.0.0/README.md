# pipeline-core
The PipelineCore repo.

# commands

## auth
- `pcore credentials|credential add|rm|ls|get|use gcp <credentials-name>`

## create radish deployment
- `pcore clusters|cluster create|rm pcloud|gcp|aws|azure <cluster-name>`

## radish cluster management
- `pcore clusters|cluster config <cluster-alias> [sub command]`:
    - `scaling-strategy|caching-strategy|routing-strategy set|get|list`
    - `gpu-pools add|rm|list|get`
