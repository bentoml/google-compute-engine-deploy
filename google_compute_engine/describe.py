import sys

from .utils import (
    generate_compute_engine_names,
    run_shell_command,
)


def describe(deployment_name, compute_engine_config, return_json=False):
    service_name, _ = generate_compute_engine_names(deployment_name)

    if not return_json:
        stdout, stderr = run_shell_command(
            [
                "gcloud",
                "compute",
                "instances",
                "describe",
                service_name,
                "--zone",
                compute_engine_config["zone"],
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
                compute_engine_config["zone"],
                "--format=json",
            ]
        )

    return stdout
