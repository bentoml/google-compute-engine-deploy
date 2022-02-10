from .deploy import build_and_push_bento
from .utils import (
    generate_compute_engine_names,
    run_shell_command,
    get_bento_tag
)


def update(bento_path, deployment_name, deployment_spec):
    bento_tag = get_bento_tag(bento_path)

    service_name, gcr_tag = generate_compute_engine_names(
        deployment_name,
        deployment_spec["project_id"],
        bento_tag.name,
        bento_tag.version,
    )

    print(f"Building and Pushing {bento_tag.name}")
    build_and_push_bento(bento_tag, gcr_tag)

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
            deployment_spec["zone"],
        ]
    )
