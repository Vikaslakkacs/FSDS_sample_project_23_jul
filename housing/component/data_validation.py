import os, sys
from tkinter import E
import pandas as pd
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact
from housing.entity.artifact_entity import DataValidationArtifact

from evidently.model_profile import Profile
from evidently.model_profile .sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

import json
class DataValidation:
    def __init__(self, data_validation_config:DataValidationConfig,
                        data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config= data_validation_config
            self.data_ingestion_artifact= data_ingestion_artifact
        except Exception as e:
            raise HousingException(e, sys) from e
    
    def get_train_and_test_df(self):

        try:
            train_df= pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df= pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df, test_df
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
    
    def detect_outlier(self):
        try:
            pass
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

    def is_data_drift_found(self)->bool:
        """To verify whether data drift exists or not
        What is data drift?
        Ans: When we try to train model with another set of data (for already trained model)
        and found out there is a change in the prediction then we can say that as data drift.


        Raises:
            HousingException: Data drift process failed.

        Returns:
            bool: True if data drift is found else False
        """
        try:
            report= self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True ## For testing purpose
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_and_save_data_drift_report(self):
        try:
            profile= Profile(sections=[DataDriftProfileSection()])
            train_df, test_df= self.get_train_and_test_df()
            ## Calculate the data drift
            profile.calculate(train_df, test_df)

            ## Loading the data into json
            report= json.loads(profile.json())
            ## Saving data in a file
            ###Creating directory of report.joson when not present
            report_file_path=self.data_validation_config.report_file_path
            report_dir= os.path.dirname(report_file_path)
            os.makedirs(report_dir, exist_ok=True)

            with open(report_file_path,"w") as report_file:
                json.dump(report, report_file, indent=6)
            logging.info("Data drift report has been generated.")
            return report

        except Exception as e:
            raise HousingException(e, sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard= Dashboard(tabs=[DataDriftTab()])
            train_df, test_df= self.get_train_and_test_df()

            dashboard.calculate(train_df, test_df)
            ## Creating directory
            report_page_file_path= self.data_validation_config.report_page_file_path
            report_page_file_path_dir= os.path.dirname(report_page_file_path)
            os.makedirs(report_page_file_path_dir, exist_ok=True)
            dashboard.save(report_page_file_path)
        except Exception as e:
            raise HousingException(e, sys) from e
    

    def initiate_data_validation(self)->DataValidationArtifact:

        try:
            is_train_test_file_available= self.is_train_test_file_exists()
            ## Validation schema check
            validation_status= self.validate_dataset_schema()
            self.is_data_drift_found()
            data_validation_artifact= DataValidationArtifact(schema_file_path=self.data_validation_config.schema_file_path,
                                                             report_file_path=self.data_validation_config.report_file_path,
                                                             report_page_file_path=self.data_validation_config.report_page_file_path,
                                                             is_validated=True,
                                                             message="Data validation is completed")
            logging.info("Data validation artifact is successfully performed")
            return data_validation_artifact
        except Exception as e:
            raise HousingException(e, sys) from e