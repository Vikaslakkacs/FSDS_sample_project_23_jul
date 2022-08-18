from multiprocessing.connection import Pipe
from housing.exception import HousingException
from housing.pipeline.pipeline import Pipeline
import os, sys
from housing.logger import logging
from housing.exception import HousingException
from housing.config.configuration import Configuration
from housing.component.data_transformation import DataTransformation

def main():
    try:
        #pipeline=Pipeline()
        #pipeline.run_pipeline()
        # config= Configuration().get_data_validation_config()
        # print(config)
        #config= Configuration()
        #print(config.get_data_transformation_config())
        schema_file_path="/Users/vikaslakka/Desktop/FSDS/Machine_learning/Projects/sample_project_12_jul/FSDS_sample_project_23_jul/config/schema.yaml"
        file_path= "/Users/vikaslakka/Desktop/FSDS/Machine_learning/Projects/sample_project_12_jul/FSDS_sample_project_23_jul/housing/artifact/data_ingestion/22-08-11-17-36-45/ingested_data/test/housing.csv"
        df= DataTransformation.load_data(file_path, schema_file_path=schema_file_path)
        print(df.dtypes)
        print(df.columns)
    except Exception as e:
        logging.error(f"{e}")
        print(e)


if __name__=="__main__":
    main()