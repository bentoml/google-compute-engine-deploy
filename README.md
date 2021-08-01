# BentoML Google Compute Engine deployment tool

![Generic badge](https://img.shields.io/badge/Release-Alpha-<COLOR>.svg)

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
    Make sure you note down the external IP to which we will be making the requests.
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
