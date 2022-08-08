from housing.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig, TrainingPipelineConfig
from housing.exception import HousingException
from housing.util.util import read_yaml_file
from housing.constant import *
import os, sys
from housing.logger import logging



class Configuration:
    """
    Configurations of the machine learning architecture are created
    """

    def __init__(self, config_file_path:str= CONFIG_FILE_PATH,
                 current_time_stamp:str=CURRENT_TIME_STAMP)-> None:
        try:
            self.config_info= read_yaml_file(file_path= config_file_path)
            self.time_stamp=CURRENT_TIME_STAMP
            self.training_pipeline_config= self.get_training_pipeline_config()
            self.data_ingestion_config= self.get_data_ingestion_config()
            self.data_validation_config=self.get_data_validation_config()
            self.data_transformation_config= self.get_data_transformation_config()
            self.model_trainer_config= self.get_model_trainer_config()
               
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_data_ingestion_config(self)-> DataIngestionConfig:
        """Generats path names related to Data ingestion. All the paths are created under artifact folder.

        Raises:
            HousingException: when path creation fails

        Returns:
            DataIngestionConfig: named tuple with all the path names
        """
        try:
            ## Path till artifact folder is stored along with current time stamp for tracking purpose
            artifact_dir= self.training_pipeline_config.artifact_dir

            data_ingestion_info= self.config_info[DATA_INGESTION_CONFIG_KEY]## Data ingestion info from yaml

            ## Joining artifact folder with data ingestion folder along with time stamp
            data_ingestion_artifact_dir= os.path.join(artifact_dir,DATA_INGESTION_ARTIFACT_DIR, self.time_stamp)
            
            dataset_download_url=data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]

            tgz_download_dir=os.path.join(data_ingestion_artifact_dir,
                                        data_ingestion_info[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY])

            raw_data_dir=os.path.join(data_ingestion_artifact_dir,
                                        data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY])

            ## For train and test it has to again store in seperate folder of ingestion data so appending
            ingestion_data_dir= os.path.join(
                                            data_ingestion_artifact_dir,
                                            data_ingestion_info[DATA_INGESTION_DIR_NAME_KEY])

            ingested_train_dir=os.path.join(ingestion_data_dir,
                                            data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY])

            ingested_test_dir=os.path.join(ingestion_data_dir,
                                            data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY])

            data_ingestion_config= DataIngestionConfig(dataset_download_url=dataset_download_url,
                                                    tgz_download_dir=tgz_download_dir,
                                                    raw_data_dir=raw_data_dir,
                                                    ingested_train_dir=ingested_train_dir,
                                                    ingested_test_dir=ingested_test_dir) 
            
            
            logging.info(f"Data ingestion config: {data_ingestion_config}")
            return  data_ingestion_config

        except Exception as e:
            raise HousingException(e, sys) from e

    def get_data_validation_config(self)-> DataValidationConfig:
        try:
            artifact_dir= self.training_pipeline_config.artifact_dir
            data_validation_info=self.config_info[DATA_VALIDATION_CONFIG_KEY]
            data_validation_artifact_dir=os.path.join(artifact_dir,DATA_VALIDATION_SCHEMA_DIR,self.time_stamp)
            schema_file_path=os.path.join(data_validation_artifact_dir, data_validation_info[DATA_VALIDATION_SCHEMA_DIR])
            
            data_validation_config=DataValidationConfig(schema_file_path=schema_file_path)
            logging.info(f"data Validaton config: {data_validation_config}")
            return data_validation_config
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_data_transformation_config(self)-> DataTransformationConfig:
        try:
            artifact_dir= self.training_pipeline_config.artifact_dir
            data_transformation_info= self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]
            data_transformation_artifact_dir= os.path.join(artifact_dir,DATA_TRANSFORMATION_TRANSFORMED_DIR, self.time_stamp)
            add_bedroom_per_room=data_transformation_info[DATA_TRANSFORMATION_ADD_BEDROOM]
            data_transformed_dir=os.path.join(data_transformation_artifact_dir,
                                               data_transformation_info[DATA_TRANSFORMATION_TRANSFORMED_DIR])
            transformed_train_dir=os.path.join(data_transformed_dir,data_transformation_info[DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR])
            transformed_test_dir=os.path.join(data_transformed_dir, data_transformation_info[DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR])
            preprocessed_object_file_path= os.path.join(data_transformed_dir, data_transformation_info[DATA_TRANSFORMATION_PREPROCESSING_DIR])


            data_transformation_config= DataTransformationConfig(add_bedroom_per_room=add_bedroom_per_room,
                                                                 transformed_train_dir=transformed_train_dir,
                                                                 transformed_test_dir=transformed_test_dir,
                                                                 preprocessed_object_file_path=preprocessed_object_file_path)
            logging.info(f"data_transformation_config: {data_transformation_config}")
            return data_transformation_config
        except Exception as e:
            raise HousingException(e, sys) from e
            
    def get_model_trainer_config(self)-> ModelTrainerConfig:
        try:
            artifact_dir= self.training_pipeline_config.artifact_dir
            data_trainer_info= self.config_info[MODEL_TRAINING_CONFIG_KEY]
            data_trainer_artifact_dir= os.path.join(artifact_dir, data_trainer_info[MODEL_TRAINING_TRAINED_MODEL_DIR], self.time_stamp)
            trained_model_file_path=data_trainer_artifact_dir
            trained_model_config_file_path=os.path.join(data_trainer_artifact_dir, data_trainer_info[MODEL_TRAINING_CONFIG_DIR])
            base_accuracy=data_trainer_info[MODEL_TRAINING_BASE_ACCURACY]

            model_training_config= ModelTrainerConfig(trained_model_file_path=trained_model_file_path,
                                                      trained_model_config_file_path=trained_model_config_file_path,
                                                      base_accuracy=base_accuracy)

            logging.info(f"model_trainer_config:{model_training_config}")
            return model_training_config
        except Exception as e:
            raise HousingException(e, sys) from e
            
    def get_model_evaluation_config(self)-> ModelEvaluationConfig:
        try:
            pass
        except Exception as e:
            raise HousingException(e, sys) from e
            
    def get_model_pusher_config(self)-> ModelPusherConfig:
        try:
            artifact_dir= self.training_pipeline_config.artifact_dir
            model_pusher_info= self.config_info[MODEL_EVALUATION_CONFIG_KEY]
            export_dir_path= self.config_info[MODEL_PUSHER_EXPORT_DIR]
            export_dir_path= os.path.join(model_pusher_info, export_dir_path)

            model_pusher_config= ModelPusherConfig(export_dir_path=export_dir_path)
        except Exception as e:
            raise HousingException(e, sys) from e
            
    def get_training_pipeline_config(self)-> TrainingPipelineConfig:
        try:
            training_pipeline_config= self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir= os.path.join(ROOT_DIR,
                                       training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
                                       training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
            training_pipeline_config= TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training pipeline config:{training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise HousingException(e, sys) from e



