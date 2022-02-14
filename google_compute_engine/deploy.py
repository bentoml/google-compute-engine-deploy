from .utils import (
    generate_compute_engine_names,
    run_shell_command,
    get_bento_tag,
    console,
    build_and_push_bento,
)




def deploy(bento_path, deployment_name, deployment_spec):
    with console.status("Deploying to Google Compute Engine") as spinner:
        bento_tag = get_bento_tag(bento_path)

        service_name, gcr_tag = generate_compute_engine_names(
            deployment_name,
            deployment_spec["project_id"],
            bento_tag.name,
            bento_tag.version,
        )

        spinner.update(f"Building and Pushing {bento_tag.name}")
        build_and_push_bento(bento_tag, gcr_tag)
        console.print(f"[b]{bento_tag.name}[/b] has been build and pushed into GCR registry!")

        spinner.update(f"Creating Cloud Engine instance [{service_name}]")
        # check if gpu is included in config
        gpu = []
        if deployment_spec.get("gpu_type") is not None:
            gpu = [
                f"--accelerator type={deployment_spec['gpu_type']},"
                f"count={deployment_spec['gpu_count']}",
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
                deployment_spec["zone"],
                "--container-image",
                gcr_tag,
                "--machine-type",
                deployment_spec["machine_type"],
                "--tags=bentoml-in",
                *gpu,
            ]
        )
        console.print("Compute Instance created!")

        spinner.update("Creating the firewall rules")
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
        console.print("Firewall rules created!")
