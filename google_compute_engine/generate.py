import os

from bentoctl.utils.operator_helpers.generate import (
    TERRAFORM_VALUES_FILE_NAME,
    Generate,
)
from bentoctl.utils.operator_helpers.values import DeploymentValues


class GCPDeploymentValues(DeploymentValues):
    @staticmethod
    def parse_image_tag(image_tag: str):
        registry_url, _, tag = image_tag.split("/")
        repo, version = tag.split(":")

        return registry_url, repo, version


class GCPGenerate(Generate):
    @staticmethod
    def generate_terraform_values(name: str, spec: dict, destination_dir: str):

        params = GCPDeploymentValues(name, spec, "terraform")

        values_file = os.path.join(destination_dir, TERRAFORM_VALUES_FILE_NAME)
        params.to_params_file(values_file)

        return values_file


generate = GCPGenerate(os.path.join(os.path.dirname(__file__), "templates"))
