import os, sys
from tkinter import E
from housing.exception import HousingException
from housing.logger import logging
from housing.entity.config_entity import DataIngestionConfig
from housing.entity.artifact_entity import DataIngestionArtifact
import tarfile ## to handle compressed files.
from six.moves import urllib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
class DataIngestion:
    """
    Consists of DataIngestion steps:
        * Downloading the data
        * extracting tgz file
        * splitting the data into train test split
        * initiating data ingestion which consists of all the methods in order.
    """

    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'=' * 20} Data ingestion log started. {'=' * 20}")
            self.data_ingestion_config= data_ingestion_config
        except Exception as e:
            raise HousingException(e, sys) from e

    

    def download_housing_data(self):
        """Downloading the data from source

        Raises:
            HousingException: Download failed

        Returns: 
            downloaded tgz file path
        """
        try:
            ## Extracting remote url to download dataset.
            download_url=self.data_ingestion_config.dataset_download_url

            ## Folder location to download file
            tgz_download_dir= self.data_ingestion_config.tgz_download_dir

            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)

            ## If folder is not present then create
            os.makedirs(tgz_download_dir, exist_ok=True)

            ## Housing file name from url
            housing_file_name= os.path.basename(download_url)

            ##Complete file path of zip file
            tgz_file_path= os.path.join(tgz_download_dir, housing_file_name)

            ###download file fro url
            logging.info(f"File downloading from url: [{download_url}] into {tgz_file_path}")
            urllib.request.urlretrieve(download_url, tgz_file_path)

            logging.info(f"Downloaded file is stored in: {tgz_file_path}")
            return tgz_file_path


        except Exception as e:
            raise HousingException(e, sys) from e
    
    def extract_tgz_file(self,tgz_file_path:str):
        """Extracts tgz_file from the folder path using tarfile package.

        Args:
            tgz_file_path (str): file location

        Raises:
            HousingException: Extraction failed
        """
        try:
            ## Getting raw data directory
            raw_data_dir= self.data_ingestion_config.raw_data_dir
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
            
            os.makedirs(raw_data_dir, exist_ok=True)
            ## opening the tar file and extracting.
            logging.info(f"Extracting tgz file from : {tgz_file_path}")
            with tarfile.open(tgz_file_path) as housing_tgz_file_path:
                housing_tgz_file_path.extractall(raw_data_dir)
            logging.info(f"Extracted to : {raw_data_dir}")

        except Exception as e:
            raise HousingException(e, sys) from e

    def split_data_as_train_test(self)->DataIngestionArtifact:
        try:
            raw_data_dir= self.data_ingestion_config.raw_data_dir

            file_name= os.listdir(raw_data_dir)[0]##File name

            housing_file_path=os.path.join(raw_data_dir, file_name)

            housing_data_frame= pd.read_csv(housing_file_path)## Reading dataset

            ## We will use stratified split to make the data split evenly with respect to features
            ## We will split the data w.r.t income category
            housing_data_frame["income_cat"]= pd.cut(
                    housing_data_frame["median_income"],
                    bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                    labels=[1, 2, 3, 4, 5]
            )
            ## Create training dataset
            strat_train_set= None
            strat_test_set= None

            ## Split variables
            split= StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
            ## provides index of test and train data 
            for train_index, test_index in split.split(housing_data_frame, housing_data_frame["income_cat"]):
                strat_train_set= housing_data_frame.loc[train_index].drop("income_cat", axis=1)
                strat_test_set= housing_data_frame.loc[test_index].drop("income_cat", axis=1)
            
            ## Ingested data directory
            train_file_path= os.path.join(self.data_ingestion_config.ingested_train_dir, file_name)
            test_file_path= os.path.join(self.data_ingestion_config.ingested_test_dir, file_name)

            ## Saving train and test information into file
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                strat_train_set.to_csv(train_file_path, index=False)
            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                strat_test_set.to_csv(test_file_path, index=False)

            ## Data ingestion artifact
            data_ingestion_artifact= DataIngestionArtifact(train_file_path=train_file_path,
                                 test_file_path= test_file_path,
                                  is_ingested= True,
                                   message= f"Data ingestion completed successfully")
            logging.info(f"DataIngestionArtifact is completed: {DataIngestionArtifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise HousingException(e, sys) from e

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            tgz_file_path= self.download_housing_data()
            logging.info(f"Downloading housing data is done")
            ##File extraction
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            logging.info(f"File Extraction is done")
            data_ingestion_artifact= self.split_data_as_train_test()
            logging.info(f"Splitting of train and test data is done")
            return data_ingestion_artifact
        except Exception as e:
            raise HousingException(e, sys) from e
    
    def __del__(self):
        logging.info(f"Data ingestion log completed")