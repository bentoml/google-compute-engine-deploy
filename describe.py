import sys

from ruamel.yaml import YAML

from utils import (
    generate_compute_engine_names,
    run_shell_command,
    get_configuration_value,
)


def describe_compute_engine(deployment_name, config_json, return_json=False):
    service_name, _ = generate_compute_engine_names(deployment_name)
    deployment_config = get_configuration_value(config_json)

    if not return_json:
        stdout, stderr = run_shell_command(
            [
                "gcloud",
                "compute",
                "instances",
                "describe",
                service_name,
                "--zone",
                deployment_config["zone"],
            ]
        )
        print(stdout)
    else:
        stdout, stderr = run_shell_command(
            [
                "gcloud",
                "compute",
                "instances",
                "describe",
                service_name,
                "--zone",
                deployment_config["zone"],
                "--format=json",
            ]
        )

        return stdout


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Please provide deployment_name and config (optional)")
    deployment_name = sys.argv[1]
    config_json = sys.argv[2] if len(sys.argv) == 3 else "cloud_run_config.json"

    describe_compute_engine(deployment_name, config_json)
