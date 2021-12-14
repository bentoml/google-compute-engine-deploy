import sys

from bentoml.saved_bundle import load_bento_service_metadata

from .utils import (
    generate_compute_engine_names,
    run_shell_command,
)


def deploy(bento_bundle_path, deployment_name, compute_engine_config):
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

    print(f"Creating Cloud Engine instance [{service_name}]")
    # check if gpu is included in config
    gpu = []
    if compute_engine_config.get("gpu_type") is not None:
        gpu = [
            f"--accelerator type={compute_engine_config['gpu_type']},"
            f"count={compute_engine_config['gpu_count']}",
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
            compute_engine_config["zone"],
            "--container-image",
            gcr_tag,
            "--machine-type",
            compute_engine_config["machine_type"],
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
    print("Deploy complete!")
