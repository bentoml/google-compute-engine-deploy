import sys

from bentoml.saved_bundle import load_bento_service_metadata

from .utils import (
    generate_compute_engine_names,
    run_shell_command,
)


def update(bento_bundle_path, deployment_name, compute_engine_config):
    bundle_metadata = load_bento_service_metadata(bento_bundle_path)

    service_name, gcr_tag = generate_compute_engine_names(
        deployment_name,
        compute_engine_config["project_id"],
        bundle_metadata.name,
        bundle_metadata.version,
    )

    print(f"Building and Pushing {bundle_metadata.name}")
    run_shell_command(
        ["gcloud", "builds", "submit", bento_bundle_path, "--tag", gcr_tag]
    )

    print(f"Updating Cloud Engine instance [{service_name}]")
    run_shell_command(
        [
            "gcloud",
            "compute",
            "instances",
            "update-container",
            service_name,
            "--container-image",
            gcr_tag,
            "--zone",
            compute_engine_config["zone"],
        ]
    )
    print("Update complete!")

