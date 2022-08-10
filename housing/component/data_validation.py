import os, sys
from tkinter import E
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact
class DataValidation:
    def __init__(self, data_validation_config:DataValidationConfig,
                        data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config= data_validation_config
            self.data_ingestion_artifact= data_ingestion_artifact
        except Exception as e:
            raise HousingException(e, sys) from e
    
    def is_train_test_file_exists(self)->bool:
        """To check whether train and test files exists in the folder

        Raises:
            HousingException: File does not exists

        Returns:
            bool: True if exists else False
        """

        try:
            is_train_file_exists=False
            is_test_file_exists=False
            ##Checking whether file exists or not
            train_file_path= self.data_ingestion_artifact.train_file_path
            test_file_path= self.data_ingestion_artifact.test_file_path

            is_train_file_exists= os.path.exists(train_file_path)
            is_test_file_exists= os.path.exists(test_file_path)
            is_available= is_train_file_exists and is_test_file_exists

            logging.info(f"Train file path exists= {is_train_file_exists} and test file path exists= {is_test_file_exists}")
            if not is_available:
                training_file= self.data_ingestion_artifact.train_file_path
                testing_file= self.data_ingestion_artifact.test_file_path
                message= f"training file: {training_file} or testing file: {testing_file} is not present"
                raise Exception(message)
            return is_available
        except Exception as e:
            raise HousingException(e, sys) from e
    
    def validate_dataset_schema(self)->bool:
        """Validation training and test file dataset using schema file
        Checks:
        * Number of columns
        * Check the values of ocean proximity
        * Verify Column names

        Raises:
            HousingException: _description_

        Returns:
            bool: _description_
        """

        try:
            validation_status= False

            validaition_status=True
            
            return validation_status
        except Exception as e:
            raise HousingException(e, sys) from e
    

    def initiate_data_validation(self):

        try:
            is_train_test_file_available= self.is_train_test_file_exists()
            
            ## Validation schema check
            validation_status= self.validate_dataset_schema()

        except Exception as e:
            raise HousingException(e, sys) from e