<div align="center">
    <h1>Google Compute Engine Operator</h1>
    <p>
        <img src="https://user-images.githubusercontent.com/5261489/153543268-8bbf11db-c0ef-4b1c-808f-1bf6fc566aa7.png" width=40%/>
    <p>
      <img src="https://img.shields.io/badge/Release-Alpha-<COLOR>.svg"/>
</div>

Google Compute Engine offers you a secure and costomizable compute service that lets you create and run virutal machines on Google's infrastructure. You can choose from a wide range of CPU, GPU and memory configurations to meet the needs of 
your models. 

<!--ts-->

## Table of Contents

   * [Prerequisites](#prerequisites)
   * [Quickstart with bentoctl](#quickstart-with-bentoctl)
   * [Quickstart with scripts](#quickstart-with-scripts)
   * [Available config options for Compute Engine deployements](#available-config-options-for-compute-engine-deployements)

<!-- Added by: jjmachan, at: Friday 11 February 2022 12:28:28 PM IST -->

<!--te-->
## Prerequisites

- An active GCP account configured on the machine with `gcloud` CLI installed and configured
  - Installation instructions: https://cloud.google.com/sdk/docs/install
  - Configuring gcloud SDK: https://cloud.google.com/sdk/docs/initializing
  - Setup the permissions - IAM permission for [Container Registry](https://cloud.google.com/container-registry/docs/access-control)
- Docker is installed and running
  - Install instruction: https://docs.docker.com/install
- install the required python packages
  - `$ pip install -r requirements.txt`

## Quickstart with bentoctl

To run this quickstart, you will need to have a working bento. You can checkout [BentoML quickstart guide](https://github.com/bentoml/gallery/tree/main) for how to get it started. After you have a bento working locally, you can now deploy it to Compute Engine with bentoctl.

1. Install bentoctl
    ```bash
    $ pip install --pre bentoctl
    ```

2. Add Google Compute Engine operator
    ```bash
    $ bentoctl operator add google-compute-engine   
    Added google-compute-engine!                                              
    ```

3. Deploy to Compute Engine using bentoctl deploy command
    ```bash
    # Use the interactive mode
    $ bentoctl deploy 

    Bentoctl Interactive Deployment Spec Builder

    Welcome! You are now in interactive mode.

    This mode will help you setup the deployment_spec.yaml file required for
    deployment. Fill out the appropriate values for the fields.

    (deployment spec will be saved to: ./deployment_spec.yaml)

    api_version: v1
    metadata: 
        name: test-script
        operator: google-compute-engine
    spec: 
      bento: testservice:esftabebw2pswho3
      project_id: bentoml-316710
      zone: us-central1-a
      machine_type: n1-standard-1
      
    deployment spec generated to: deployment_spec.yaml
    ~ Builing and Pushing Image
    ~ Deploying Image
    Successful deployment!

4. Get deployment information
    ```bash
    $ bentoctl describe -f deployment_spec.yaml
    {
      "cpuPlatform": "Intel Haswell",
      "creationTimestamp": "2022-02-10T05:28:22.979-08:00",
      "id": "6912383771654794265",
      "kind": "compute#instance",
      "labels": {
        "container-vm": "cos-stable-93-16623-102-8"
      },
      "lastStartTimestamp": "2022-02-10T05:28:32.725-08:00",
      "machineType": "https://www.googleapis.com/compute/v1/projects/bentoml-316710/zones/us-central1-a/machineTypes/n1-standard-1",
      "name": "testservice",
      "networkInterfaces": [
        {
          "accessConfigs": [
            {
              "kind": "compute#accessConfig",
              "name": "external-nat",
              "natIP": "34.72.117.169",
              "networkTier": "PREMIUM",
              "type": "ONE_TO_ONE_NAT"
            }
          ],
          "fingerprint": "KZzYSIeZXrI=",
          "kind": "compute#networkInterface",
          "name": "nic0",
          "network": "https://www.googleapis.com/compute/v1/projects/bentoml-316710/global/networks/default",
          "networkIP": "10.128.0.7",
          "stackType": "IPV4_ONLY",
          "subnetwork": "https://www.googleapis.com/compute/v1/projects/bentoml-316710/regions/us-central1/subnetworks/default"
        }
      ],
      "status": "RUNNING",
      "zone": "https://www.googleapis.com/compute/v1/projects/bentoml-316710/zones/us-central1-a"
    }

    ```
    Make sure you note down the external IP to which we will be making the
    requests. Once you have that to head over to port 5000 with that IP in the
    browser to see the swagger UI to try out the various endpoints or use curl
    to make requests.
    
5. Make sample request
    ```bash
    $ curl -i \
      --header "Content-Type: application/json" \
      --request POST \
      --data '[[5.1, 3.5, 1.4, 0.2]]' \
      http://34.66.39.137:5000/predict


    # Sample output
    HTTP/1.1 200 OK
    Content-Type: application/json
    Content-Length: 3
    Connection: keep-alive
    Date: Tue, 21 Jan 2020 22:43:17 GMT
    
    [0]%
    ```

6. Delete deployment with bentoctl
    ```bash
    $ bentoctl delete -f deployment_spec.yaml
    
## Quickstart with scripts

1. Build and save Bento Bundle from [BentoML quick start guide](https://github.com/bentoml/BentoML/blob/master/guides/quick-start/bentoml-quick-start-guide.ipynb)

2. Create Compute Engine deployment with the deployment tool

    Run deploy script in the command line:

    ```bash
    $ BENTO_BUNDLE_PATH=$(bentoml get IrisClassifier:latest --print-location -q)
    $ ./deploy $BENTO_BUNDLE_PATH iristest compute_engine_config.json

    # Sample output
    Building and Pushing IrisClassifier
    Creating the firewall rules
    Creating Cloud Engine instance [iristest]
    Deploy complete!
    ```



    Get Compute Engine deployment information and status

    ```bash
    $ ./describe iristest
    ```
    Make sure you note down the external IP to which we will be making the
    requests. Once you have that to head over to port 5000 with that IP in the
    browser to see the swagger UI to try out the various endpoints or use curl
    to make requests.
    
3. Make sample request against deployed service

    ```bash
    $ curl -i \
      --header "Content-Type: application/json" \
      --request POST \
      --data '[[5.1, 3.5, 1.4, 0.2]]' \
      http://34.66.39.137:5000/predict

    # Sample output
    HTTP/1.1 200 OK
    Content-Type: application/json
    Content-Length: 3
    Connection: keep-alive
    Date: Tue, 21 Jan 2020 22:43:17 GMT
    
    [0]%
    ```

4. Delete Compute Engine deployment

    ```bash
    ./delete iristest
    ```
    

## Available config options for Compute Engine deployements
* `project_id`: The project ID for the GCP project you want to deploy to. Make sure the VM intances API is activated. 
* `zone`: The zone to which you want to deploy to. To get the complete list of available zones run `gcloud compute zones list`
* `machine_type`: This specifies the machine type you want to use. You can use different machine types based on the resource requirments of your model. To get a list of all the machine types available run `gcloud compute machine-types list`
* `gpu_type`: Cloud compute also has support for adding GPU to the VM. Do note
that that the gpu types you can use depends on your location and the machine
type you have set. Check the [docs for
google](https://cloud.google.com/compute/docs/gpus#restrictions) for more info.
To get the list of all the GPU types supported run `gcloud compute
accelerator-types list`
* `gpu_count`: The number of GPUs you want to add to your VM instance.
