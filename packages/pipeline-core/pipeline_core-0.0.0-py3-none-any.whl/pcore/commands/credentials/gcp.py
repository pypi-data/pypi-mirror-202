import argparse
import json
import os

from google.oauth2 import service_account
from pipeline.configuration import current_configuration


def add_credentials(namespace: argparse.Namespace) -> None:
    service_account_path: str = namespace.service_account_path
    project_id: str = namespace.project_id

    if service_account_path is None:
        service_account_path = input("Please paste your service file path:\n")

    service_account_path = os.path.expanduser(service_account_path)

    if not os.path.exists(service_account_path):
        raise FileNotFoundError(
            f"Service account file not found: {service_account_path}"
        )

    with open(service_account_path, "r") as f:
        service_account_data = json.loads(f.read())

    print(f"Adding GCP service account auth from: '{service_account_path}'")
    service_account.Credentials.from_service_account_info(service_account_data)

    current_configuration.set_google_auth(
        service_account=service_account_data, project_id=project_id
    )
