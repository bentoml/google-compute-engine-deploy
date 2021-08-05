import sys

from bentoml.saved_bundle import load_bento_service_metadata

from utils import (
    get_configuration_value,
    generate_compute_engine_names,
    run_shell_command,
)


def deploy_to_compute_engine(bento_bundle_path, deployment_name, config_json):
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

    print(f"Creating Cloud Engine instance [{service_name}]")
    # check if gpu is included in config
    gpu = []
    if deployment_config.get("gpu_type") is not None:
        gpu = [
            f"--accelerator type={deployment_config['gpu_type']},"
            f"count={deployment_config['gpu_count']}",
            "--maintenace-policy TERMINATE",
        ]
    run_shell_command(
        [
            "gcloud",
            "compute",
            "instances",
            "create-with-container",
            service_name,
            "--zone",
            deployment_config["zone"],
            "--container-image",
            gcr_tag,
            "--machine-type",
            deployment_config["machine_type"],
            "--tags=bentoml-in",
            *gpu,
        ]
    )

    print("Creating the firewall rules")
    run_shell_command(
        [
            "gcloud",
            "compute",
            "firewall-rules",
            "create",
            "allow-bentoml",
            "--action=ALLOW",
            "--rules=tcp:5000",
            "--source-ranges=0.0.0.0/0",
            "--target-tags=bentoml-in",
        ]
    )


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise Exception(
            "Please provide bento_bundle_path deployment_name and configuration json"
        )
    bento_bundle_path = sys.argv[1]
    deployment_name = sys.argv[2]
    config_json = sys.argv[3] if sys.argv[3] else "cloud_engine_config.json"

    deploy_to_compute_engine(bento_bundle_path, deployment_name, config_json)
    print("Deploy complete!")
