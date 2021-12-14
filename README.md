# BentoML Google Compute Engine deployment tool

![Generic badge](https://img.shields.io/badge/Release-Alpha-<COLOR>.svg)

YOU GOTTA SET IAM PERMISSIONS. READ HERE https://cloud.google.com/container-registry/docs/access-control

GOTTA ENABLE THIS
unknown: Service 'containerregistry.googleapis.com' is not enabled for consumer 'project:comp-eng-333821'.
Pushing gcr.io/comp-eng-333821/irisclassifier:20210923152106_c95f2e
The push refers to repository [gcr.io/comp-eng-333821/irisclassifier]

ENABLE CLOUD BUILD API

GIVE STORAGE ADMIN RLE UNDER IAM & ADMIN
https://stackoverflow.com/questions/51410633/service-account-does-not-have-storage-objects-get-access-for-google-cloud-storag

Go here for this
https://console.cloud.google.com/projectselector2/apis/api/containerregistry.googleapis.com/overview?supportedpurview=project&authuser=1
https://stackoverflow.com/questions/68139665/unknown-service-containerregistry-googleapis-com-is-not-enabled-for-consumer

SHIFT YOUR GCLOUD PROJECT 
https://stackoverflow.com/questions/57194481/why-dont-i-have-access-to-anything-in-my-gcp-project



Google Compute Engine offers you a secure and costomizable compute service that lets you create and run virutal machines on Google's infrastructure. You can choose from a wide range of CPU, GPU and memory configurations to meet the needs of 
your models. 

## Prerequisites

- An active GCP account configured on the machine with `gcloud` CLI installed and configured
  - Installation instructions: https://cloud.google.com/sdk/docs/install
  - Configuring gcloud SDK: https://cloud.google.com/sdk/docs/initializing
- Docker is installed and running
  - Install instruction: https://docs.docker.com/install
- install the required python packages
  - `$ pip install -r requirements.txt`

## Deploy IrisClassifier from Bentoml quick start guide to Google Compute Engine

1. Build and save Bento Bundle from [BentoML quick start guide](https://github.com/bentoml/BentoML/blob/master/guides/quick-start/bentoml-quick-start-guide.ipynb)

2. Create Compute Engine deployment with the deployment tool

    Run deploy script in the command line:

    ```bash
    $ BENTO_BUNDLE_PATH=$(bentoml get IrisClassifier:latest --print-location -q)
    $ python deploy.py $BENTO_BUNDLE_PATH iristest ec2_config.json

    # Sample output
    Building and Pushing IrisClassifier
    Creating the firewall rules
    Creating Cloud Engine instance [iristest]
    Deploy complete!
    ```



    Get Compute Engine deployment information and status

    ```bash
    $ python describe.py iristest
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
    python delete.py iristest
    ```
    
## Deployment operations

### Create a deployment

Use command line

```bash
python deploy.py <Bento_bundle_path> <Deployment_name> <Config_JSON default is cloud_engine_config.json>
```

Example:

```bash
MY_BUNDLE_PATH=${bentoml get IrisClassifier:latest --print-location -q)
python deploy.py $MY_BUNDLE_PATH my_first_deployment cloud_engine_config.json
```

Use Python API

```python
from deploy import deploy_to_compute_engine

deploy_to_compute_engine(BENTO_BUNDLE_PATH, DEPLOYMENT_NAME, CONFIG_JSON)
```

#### Available config options for Compute Engine deployements
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

### Update a deployment

Use command line

```bash
python update.py <Bento_bundle_path> <Deployment_name> <Config_JSON>
```

Use Python API

```python
from update import update_compute_engine
update_compute_engine(BENTO_BUNDLE_PATH, DEPLOYMENT_NAME, CONFIG_JSON)
```

### Get deployment's status and information

Use command line

```bash
python describe.py <Deployment_name> <Config_JSON>
```

Use Python API

```python
from describe import describe_compute_engine
describe_compute_engine(DEPLOYMENT_NAME, CONFIG_JSON, return_json=False)
```
The `return_json` flag is used to specify if you want the output to be json formated.

### Delete deployment

Use command line

```bash
python delete.py <Deployment_name> <Config_JSON>
```

Use Python API

```python
from  delete import delete_compute_engine
delete_compute_engine(DEPLOYMENT_NAME, CONFIG_JSON)
```
