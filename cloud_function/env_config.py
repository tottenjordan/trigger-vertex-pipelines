
PROJECT_ID             = "hybrid-vertex"
PROJECT_NUM            = "934903580331"

REGION                 = "us-central1"
BQ_REGION              = "US"
BQ_PUBLIC_DS_URI       = "projects/934903580331/global/networks/ucaip-haystack-vpc-network"
DATASET_ID             = "census_pipe_triggers_v1"
VIEW_NAME              = "census_data"
BQ_LOG_DATA_URI        = "hybrid-vertex.census_pipe_triggers_v1.census_training_table"

VPC_NETWORK_NAME       = "ucaip-haystack-vpc-network"
VPC_NETWORK_FULL       = "projects/934903580331/global/networks/ucaip-haystack-vpc-network"

SERVICE_ACCOUNT        = "934903580331-compute@developer.gserviceaccount.com"

VERSION                = "v1"
PREFIX                 = "pipe-triggers-v1"

BUCKET_NAME            = "pipe-triggers-v1-hybrid-vertex"
BUCKET_URI             = "gs://pipe-triggers-v1-hybrid-vertex"

TOPIC_PATH             = "projects/hybrid-vertex/topics/pipe-triggers-v1-topic"
PUBSUB_TOPIC           = "projects/hybrid-vertex/topics/pipe-triggers-v1-topic"

PIPELINE_DISPLAY_NAME  = "census-pipe-triggers-v1"
PIPELINE_ROOT_PATH     = "gs://pipe-triggers-v1-hybrid-vertex/census_pipeline_root"
PIPELINE_YAML_FILENAME = "pipeline.yaml"
PIPELINES_FILEPATH     = "gs://pipe-triggers-v1-hybrid-vertex/census_pipeline_root/pipeline-spec/pipeline.yaml"
