from .deploy import build_and_push_bento
from .utils import (
    generate_compute_engine_names,
    run_shell_command,
    get_bento_tag,
    console,
)


def update(bento_path, deployment_name, deployment_spec):
    # start spinner
    spinner = console.status(f"Updating {deployment_name}")
    spinner.start()

    bento_tag = get_bento_tag(bento_path)

    service_name, gcr_tag = generate_compute_engine_names(
        deployment_name,
        deployment_spec["project_id"],
        bento_tag.name,
        bento_tag.version,
    )

    spinner.update(f"Building and Pushing {bento_tag.name}")
    build_and_push_bento(bento_tag, gcr_tag)
    console.print("Image build and pushed to Container Registry.")

    spinner.update(f"Updating Compute Engine instance [{service_name}]")
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
            deployment_spec["zone"],
        ]
    )
    console.print("Updated Compute Engine")
