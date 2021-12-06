import sys

from bentoml.saved_bundle import load_bento_service_metadata

from .utils import (
    get_configuration_value,
    generate_compute_engine_names,
    run_shell_command,
)


def update(bento_bundle_path, deployment_name, config_json):
    bundle_metadata = load_bento_service_metadata(bento_bundle_path)
    deployment_config = get_configuration_value(config_json)

    service_name, gcr_tag = generate_compute_engine_names(
        deployment_name,
        deployment_config["project_id"],
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
            deployment_config["zone"],
        ]
    )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise Exception(
            "Please provide bundle path, deployment name and path to Cloud Run "
            "config file (optional)"
        )
    bento_bundle_path = sys.argv[1]
    deployment_name = sys.argv[2]
    config_json = sys.argv[3] if len(sys.argv) == 4 else "cloud_run_config.json"

    update(bento_bundle_path, deployment_name, config_json)
    print("Update complete!")
