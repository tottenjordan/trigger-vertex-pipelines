import base64
import json
import time

from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import google.cloud.aiplatform as aiplatform

import kfp
from kfp import compiler, dsl
from kfp.dsl import Artifact, Dataset, Input, Metrics, Model, Output, component

from . import env_config as env_config

RETRAIN_THRESHOLD = 10 # Change this based on your use case
################################################################################
project_id = env_config.PROJECT_ID    # 'hybrid-vertex'
dataset_id = env_config.DATASET_ID    # 'census_{PREFIX}'.replace("-","_")
view_name  = env_config.VIEW_NAME     # 'census_data'

REGION             = env_config.REGION              # "us-central1"
PIPELINE_ROOT      = env_config.PIPELINE_ROOT_PATH  # "gs://trigger-pipes-v3-hybrid-vertex/census_pipeline"
PIPELINE_SPEC_PATH = env_config.PIPELINES_FILEPATH  # "gs://trigger-pipes-v3-hybrid-vertex/pipe-yaml-root/pipeline.yaml"
VERTEX_SA          = env_config.SERVICE_ACCOUNT     # '934903580331-compute@developer.gserviceaccount.com'

PIPELINE_PARAMETERS = {
      'project_id': project_id,
      'dataset_id': dataset_id,
      'view_name': view_name,
    }

bq_client = bigquery.Client(
    project=env_config.PROJECT_ID, 
    location=env_config.BQ_REGION
)
################################################################################

def insert_bq_data(table_id, num_rows):
    rows_to_insert = [
        {u"num_rows_last_retraining": num_rows, u"last_retrain_time": time.time()}
    ]

    errors = bq_client.insert_rows_json(table_id, rows_to_insert)
    if errors == []:
        print("New rows have been added.")
    else:
        print(f"Encountered errors while inserting rows: {errors}")

def create_count_table(table_id, num_rows):
    schema = [
        bigquery.SchemaField("num_rows_last_retraining", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("last_retrain_time", "TIMESTAMP", mode="REQUIRED")
    ]
    table = bigquery.Table(table_id, schema=schema)
    table = bq_client.create_table(table)
    print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")

    insert_bq_data(table_id, num_rows)

def create_pipeline_run():
    print('Kicking off a pipeline run...')

    TIMESTAMP = time.strftime("%Y%m%d-%H%M%S")
    PIPELINE_NAME = f"{env_config.PIPELINE_DISPLAY_NAME}-{TIMESTAMP}"
    
    REGION = "us-central1" # Change this to the region you want to run in
    aiplatform.init(
        project=project_id,
        location=REGION,
    )
    try:
        job = aiplatform.PipelineJob(
            display_name=f"{PIPELINE_NAME}",
            template_path=PIPELINE_SPEC_PATH,
            pipeline_root=PIPELINE_ROOT,
            parameter_values=PIPELINE_PARAMETERS
            )
        response = job.run(
            sync=False,
            service_account=VERTEX_SA,
            # network=f'projects/{PROJECT_NUM}/global/networks/{VPC_NETWORK_NAME}'
        )
        return response
    except:
        print("Error trying to run the pipeline")
        raise

# This should be the entrypoint for your Cloud Function
def check_table_size(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
          event (dict): Event payload.
          context (google.cloud.functions.Context): Metadata for the event.
    """
    # # decode the event payload string
    # payload_message = base64.b64decode(event['data']).decode('utf-8')
    # # parse payload string into JSON object
    # payload_json = json.loads(payload_message)

    data_table = bq_client.get_table(f"{project_id}.{dataset_id}.census_training_table")
    current_rows = data_table.num_rows
    print(f"{data_table.table_id} table has {current_rows} rows")
  
    # See if `count` table exists in dataset
    try:
        count_table = bq_client.get_table(f"{project_id}.{dataset_id}.count")
        print("Count table exists, querying to see how many rows at last pipeline run")

    except NotFound:
        print("No count table found, creating one...")
        create_count_table(f"{project_id}.{dataset_id}.count", current_rows)

    query_job = bq_client.query(
        f"""
        SELECT num_rows_last_retraining FROM `{project_id}.{dataset_id}.count`
        ORDER BY last_retrain_time DESC
        LIMIT 1"""
    )

    results = query_job.result()
    for i in results:
        last_retrain_count = i[0]

    rows_added_since_last_pipeline_run = current_rows - last_retrain_count
    print(f"{rows_added_since_last_pipeline_run} rows have been added since we last ran the pipeline")

    if (rows_added_since_last_pipeline_run >= RETRAIN_THRESHOLD):
        pipeline_result = create_pipeline_run()
        insert_bq_data(f"{bq_client.project}.{dataset_id}.count", current_rows)
    else:
        return f"No BigQuery data given"