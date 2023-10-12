# trigger-vertex-pipelines

## Trigger a pipeline run with Cloud Pub/Sub

* complete steps in `00-setup-env.ipynb` to setup cloud resources, grant IAM permissions, and define naming conventions used throughout this tutorial 
* run `01-pipeline-for-triggering.ipynb` to compile and deploy a model training and deployment pipeline
* follow steps in `02-create-trigger.ipynb` to deploy a Cloud Function to trigger your pipeline via PuBSub

### Train and deploy pipeline

![alt text](https://github.com/tottenjordan/trigger-vertex-pipelines/blob/main/imgs/pipeline.png)

* use Vertex AI Pipelines and KFP 2.x version of Google Cloud Pipeline Components to train and deploy an XGBoost model
* pipeline steps:
> * Create a BigQuery Dataset resource.
> * Export the dataset.
> * Train an XGBoost Model resource.
> * Create an Endpoint resource.
> * Deploys the Model resource to the Endpoint resource.

> **TODO**

### Cloud Function for triggering pipeline

![alt text](https://github.com/tottenjordan/trigger-vertex-pipelines/blob/main/imgs/cf_trigger_console.png)

* Create a Cloud Function that triggers a pipeline using an Event-Driven Cloud Function with a Cloud Pub/Sub trigger
* The Cloud Function will subscribe to a PubSub topic
* When this function is invoked, it will scan a BigQuery dataset table and kick-off a pipeline if the number of rows has increased above a threshold since last checking 

> **TODO**