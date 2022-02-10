import sys

from ruamel.yaml import YAML

from .utils import (
    get_configuration_value,
    generate_compute_engine_names,
    run_shell_command,
)
from .describe import describe


def delete(deployment_name, deployment_spec):
    service_name, _ = generate_compute_engine_names(deployment_name)
    # get the image name for container in compute engine
    service_data = describe(service_name, deployment_spec)
    yaml = YAML()
    repo_name = ''
    for item in service_data["metadata"]["items"]:
        if item["key"] == "gce-container-declaration":
            img_info = yaml.load(item["value"])
            # get the image name from the long description
            img = img_info.get('spec').get('containers')[0].get('image')
            repo_name = img.split(":")[0]

    print(f"Deleting Cloud Engine instance {service_name}")
    run_shell_command(
        [
            "gcloud",
            "compute",
            "instances",
            "delete",
            service_name,
            "--quiet",
            "--zone",
            deployment_spec["zone"],
        ]
    )

    print("Deleting firewall rules")
    run_shell_command(
        ["gcloud", "compute", "firewall-rules", "delete", "allow-bentoml", "--quiet"]
    )

    # get all images in container registry
    images, _ = run_shell_command(
        ["gcloud", "container", "images", "list-tags", repo_name, "--format=json"],
    )

    # loop through all the images in the container registry and delete them.
    for i, img in enumerate(images):
        print(f"\rDeleting image {i+1}/{len(images)}", end="")
        run_shell_command(
            [
                "gcloud",
                "container",
                "images",
                "delete",
                f"{repo_name}@{img['digest']}",
                "--force-delete-tags",
                "--quiet",
            ]
        )
    print("Deleted!")
