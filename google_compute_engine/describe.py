from .utils import (
    generate_compute_engine_names,
    run_shell_command,
)


def describe(deployment_name, deployment_spec):
    service_name, _ = generate_compute_engine_names(deployment_name)

    info_dict, _ = run_shell_command(
        [
            "gcloud",
            "compute",
            "instances",
            "describe",
            service_name,
            "--zone",
            deployment_spec["zone"],
            "--format=json",
        ]
    )
    
    return info_dict
