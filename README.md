<div align="center">
    <h1>Google Compute Engine Operator</h1>
</div>

Google Compute Engine offers you a secure and costomizable compute service that lets you create and run virutal machines on Google's infrastructure. You can choose from a wide range of CPU, GPU and memory configurations to meet the needs of your models. With the combination of [BentoML](https://github.com/bentoml/BentoML) and [bentoctl](https://github.com/bentoml/bentoctl), you can easily deploy models created with your favourite ML frameworks and easily manage the infrastructure via terraform.

> **Note:** This operator is compatible with BentoML version 1.0.0 and above. For older versions, please switch to the branch `pre-v1.0` and follow the instructions in the README.md.


## Table of Contents

   * [Quickstart with bentoctl](#quickstart-with-bentoctl)
   * [Configuration Options](#configuration-options)

## Quickstart with bentoctl

This quickstart will walk you through deploying a bento into Google Compute Engine. Make sure to go through the [prerequisites](#prerequisites) section and follow the instructions to set everything up.

### Prerequisites

1. Google cloud CLI tool - Install instruction: https://cloud.google.com/sdk/docs/install and make sure all your `gcloud` components are up to date. Run `gcloud components update` to update
2. Terraform - Terraform is a tool for building, configuring, and managing infrastructure. Installation instruction: www.terraform.io/downloads
3. Docker - Install instruction: https://docs.docker.com/install
4. A working bento - for this guide, we will use the iris-classifier bento from the BentoML [quickstart guide](https://docs.bentoml.org/en/latest/quickstart.html#quickstart).

### Steps
1. Install bentoctl via pip
    ```bash
    pip install --pre bentoctl
    ```

2. Install the operator

    Bentoctl will install the official Google Compute Engine operator and its dependencies. The Operator contains the Terraform templates and sets up the registries reqired to deploy to GCP.

    ```bash
    bentoctl operator install google-compute-engine
    ```

3. Initialize deployment with bentoctl

    Follow the interactive guide to initialize the deployment project.

    ```bash
    $ bentoctl init
    
    Bentoctl Interactive Deployment Config Builder

    Welcome! You are now in interactive mode.

    This mode will help you set up the deployment_config.yaml file required for
    deployment. Fill out the appropriate values for the fields.

    (deployment config will be saved to: ./deployment_config.yaml)

    api_version: v1
    name: quickstart
    operator: google-compute-engine
    template: terraform
    spec:
        project_id: bentoml-316710
        zone: us-central1-a
        machine_type: n1-standard-1
    filename for deployment_config [deployment_config.yaml]:
    deployment config generated to: deployment_config.yaml
    ✨ generated template files.
      - ./main.tf
      - ./bentoctl.tfvars
    ```
    This will also run the `bentoctl generate` command for you and will generate the `main.tf` terraform file, which specifies the resources to be created and the `bentoctl.tfvars` file which contains the values for the variables used in the `main.tf` file.

4. Build and push docker image into Google Container Registry.

    ```bash
    bentoctl build -b iris_classifier:latest -f deployment_config.yaml
    ```
    The iris-classifier service is now built and pushed into the container registry and the required terraform files have been created. Now we can use terraform to perform the deployment.
    
5. Apply Deployment with Terraform

   1. Initialize terraform project. This installs the Google Cloud provider and sets up the terraform folders.
        ```bash
        terraform init
        ```

   2. Apply terraform project to create compute engine deployment

        ```bash
        terraform apply -var-file=bentoctl.tfvars -auto-approve
        ```

6. Test deployed endpoint

    The `iris_classifier` uses the `/classify` endpoint for receiving requests so the full URL for the classifier will be in the form `{EndpointUrl}/classify`.

    ```bash
    URL=$(terraform output -json | jq -r .Endpoint.value)/classify
    curl -i \
      --header "Content-Type: application/json" \
      --request POST \
      --data '[5.1, 3.5, 1.4, 0.2]' \
      $URL
    ```

7. Delete deployment
    Use the `bentoctl destroy` command to remove the registry and the deployment

    ```bash
    bentoctl destroy -f deployment_config.yaml
    ```


    

## Configuration Options
* `project_id`: The project ID for the GCP project you want to deploy to. Make sure the VM intances API is activated. 
* `zone`: The zone to which you want to deploy to. To get the complete list of available zones run `gcloud compute zones list`
* `machine_type`: This specifies the machine type you want to use. You can use different machine types based on the resource requirments of your model. To get a list of all the machine types available run `gcloud compute machine-types list`
