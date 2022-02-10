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

    IMPORTANT_PARAMS = [
        "cpuPlatform",
        "creationTimestamp",
        "id",
        "kind",
        "labels",
        "lastStartTimestamp",
        "machineType",
        "metadata",
        "name",
        "networkInterfaces",
        "status",
        "zone",
    ]

    deployment_info = {}
    for param in IMPORTANT_PARAMS:
        deployment_info[param] = info_dict[param]

    return deployment_info
