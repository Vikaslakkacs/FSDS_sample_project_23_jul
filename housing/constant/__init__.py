import os
import datetime
##getting root directory
ROOT_DIR= os.getcwd()

CONFIG_DIR= "config"
CONFIG_FILE_NAME= "config.yaml"
CONFIG_FILE_PATH= os.path.join(ROOT_DIR, CONFIG_DIR, CONFIG_FILE_NAME)
CURRENT_TIME_STAMP= f"{datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S')}"

## Training pipeline related variables
TRAINING_PIPELINE_CONFIG_KEY= "training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY= "artifact_dir"
TRAINING_PIPELINE_NAME_KEY= "pipeline_name"


### Data ingestion related variables
DATA_INGESTION_CONFIG_KEY="data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR="data_ingestion"
DATA_INGESTION_DOWNLOAD_URL_KEY="dataset_download_url"
DATA_INGESTION_RAW_DATA_DIR_KEY="raw_data_dir"
DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY="tgz_download_dir"
DATA_INGESTION_DIR_NAME_KEY="ingested_dir"
DATA_INGESTION_TRAIN_DIR_KEY="ingested_train_dir"
DATA_INGESTION_TEST_DIR_KEY="ingested_test_dir"


### Data Validation realted variables

DATA_VALIDATION_CONFIG_KEY="data_validation_config"
DATA_VALIDATION_SCHEMA_DIR="schema_dir"
DATA_VALIDATION_SCHEMA_FILE_NAME="schema_file_name"
DATA_VALIDATION_REPORT_FILE_NAME="report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME="report_page_file_name"

### Data Transformation related variables
DATA_TRANSFORMATION_CONFIG_KEY="data_transformation_config"
DATA_TRANSFORMATION_ADD_BEDROOM="add_bedroom_per_room"
DATA_TRANSFORMATION_TRANSFORMED_DIR="transformed_dir"
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR="transformed_train_dir"
DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR="transformed_test_dir"
DATA_TRANSFORMATION_PREPROCESSING_DIR="preprocessing_dir"
DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME="preprocessed_object_file_name"


## Model Training related variables
MODEL_TRAINING_CONFIG_KEY="model_trainer_config"
MODEL_TRAINING_TRAINED_MODEL_DIR="trained_model_dir"
MODEL_TRAINING_MODEL_FILE_NAME="model_file_name"
MODEL_TRAINING_BASE_ACCURACY="base_accuracy"
MODEL_TRAINING_CONFIG_DIR="model_config_dir"
MODEL_TRAINING_CONFIG_FILE_NAME="model_config_file_name"


## Model Evaluation related variables
MODEL_EVALUATION_CONFIG_KEY="model_evaluation_config"
MODEL_EVALUATION_FILE_NAME="model_evaluation_file_name"

### Model Pusher related variables
MODEL_PUSHER_CONFIG_KEY="model_pusher_config"
MODEL_PUSHER_EXPORT_DIR="model_export_dir"