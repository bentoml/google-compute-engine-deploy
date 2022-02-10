import subprocess
import json
import re
import os

import fs
import docker
from rich.console import Console
from bentoml.bentos import Bento

# initialize the rich console for the project
console = Console(highlight=False)

def run_shell_command(command, cwd=None, env=None, shell_mode=False):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=shell_mode,
        cwd=cwd,
        env=env,
    )
    stdout, stderr = proc.communicate()
    if proc.returncode == 0:
        try:
            return json.loads(stdout.decode("utf-8")), stderr.decode("utf-8")
        except json.JSONDecodeError:
            return stdout.decode("utf-8"), stderr.decode("utf-8")
    else:
        raise Exception(
            f'Failed to run command {" ".join(command)}: {stderr.decode("utf-8")}'
        )


def push_image(repository, image_tag=None, username=None, password=None):
    docker_client = docker.from_env()
    docker_push_kwags = {"repository": repository, "tag": image_tag}
    if username is not None and password is not None:
        docker_push_kwags["auth_config"] = {"username": username, "password": password}
    try:
        docker_client.images.push(**docker_push_kwags)
    except docker.errors.APIError as error:
        raise Exception(f"Failed to push docker image: {error}")


def get_configuration_value(config_file):
    with open(config_file, "r") as file:
        configuration = json.loads(file.read())
    return configuration


def generate_compute_engine_names(
    deployment_name, project_id=None, bento_name=None, bento_version=None
):
    "Generate the service name and grc tag that is used for deployments"

    service_name = re.sub("[^a-z0-9-]", "-", deployment_name.lower())
    gcr_tag = re.sub(
        "[^a-z0-9-:_]./",
        "-",
        f"gcr.io/{project_id}/{bento_name}:{bento_version}".lower(),
    )

    return service_name, gcr_tag


def get_bento_tag(path: str):
    bento = Bento.from_fs(fs.open_fs(path))
    return bento.tag


def get_metadata(path: str):
    metadata = {}

    bento = Bento.from_fs(fs.open_fs(path))
    metadata["tag"] = bento.tag
    metadata["bentoml_version"] = ".".join(bento.info.bentoml_version.split(".")[:3])

    python_version_txt_path = "env/python/version.txt"
    python_version_txt_path = os.path.join(path, python_version_txt_path)
    with open(python_version_txt_path, "r") as f:
        python_version = f.read()
    metadata["python_version"] = ".".join(python_version.split(".")[:2])

    return metadata
