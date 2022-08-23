
import os, sys
from ssl import OP_NO_RENEGOTIATION
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataTransformationConfig
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from housing.util.util import (read_yaml_file, save_object, save_numpy_array_data,
                                 load_numpy_array_data, load_data)
from housing.constant import *




class FeatureGenerator(BaseEstimator, TransformerMixin):
    """Generation of New features for dataset

    Args:
        BaseEstimator (_type_): No args
        TransformerMixin (_type_): No args
    """

    def __init__(self, add_bedrooms_per_room=True,
                 total_rooms_ix=3,
                 population_ix=5,
                 households_ix=6,
                 total_bedrooms_ix=4, columns=None):
        """
        FeatureGenerator Initialization
        add_bedrooms_per_room: bool
        total_rooms_ix: int index number of total rooms columns
        population_ix: int index number of total population columns
        households_ix: int index number of  households columns
        total_bedrooms_ix: int index number of bedrooms columns
        """
        try:
            self.columns = columns
            if self.columns is not None:
                total_rooms_ix = self.columns.index(COLUMN_TOTAL_ROOMS)
                population_ix = self.columns.index(COLUMN_POPULATION)
                households_ix = self.columns.index(COLUMN_HOUSEHOLDS)
                total_bedrooms_ix = self.columns.index(COLUMN_TOTAL_BEDROOM)

            self.add_bedrooms_per_room = add_bedrooms_per_room
            self.total_rooms_ix = total_rooms_ix
            self.population_ix = population_ix
            self.households_ix = households_ix
            self.total_bedrooms_ix = total_bedrooms_ix
        except Exception as e:
            raise HousingException(e, sys) from e

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        try:
            room_per_household = X[:, self.total_rooms_ix] / \
                                 X[:, self.households_ix]
            population_per_household = X[:, self.population_ix] / \
                                       X[:, self.households_ix]
            if self.add_bedrooms_per_room:
                bedrooms_per_room = X[:, self.total_bedrooms_ix] / \
                                    X[:, self.total_rooms_ix]
                generated_feature = np.c_[
                    X, room_per_household, population_per_household, bedrooms_per_room]
            else:
                generated_feature = np.c_[
                    X, room_per_household, population_per_household]

            return generated_feature
        except Exception as e:
            raise HousingException(e, sys) from e


class DataTransformation:

    def __init__(self, data_transformation_config: DataTransformationConfig,
                        data_ingestion_artifact:DataIngestionArtifact,
                        data_validation_artifact:DataValidationArtifact):
        
        try:
            self.data_transformation_config= data_transformation_config
            self.data_ingestion_artifact= data_ingestion_artifact
            self.data_validation_artifact= data_validation_artifact
        except Exception as e:
            raise HousingException(e, sys) from e


    def get_transformer_object(self)->ColumnTransformer:
        """Creating pipeline which transformes both numerical and categorical objects

        Raises:
            HousingException: Column transformation of pipeline cannot be done

        Returns:
            ColumnTransformer: ColumnTransformer which consists of pipelines
        """

        try:
            schema_file_path= self.data_validation_artifact.schema_file_path

            dataset_schema=read_yaml_file(schema_file_path)
            numerical_columns=dataset_schema[NUMERICAL_COLUMN_KEY]
            categorical_columns= dataset_schema[CATEGOTICAL_COLUMN_KEY]

            num_pipeline= Pipeline(steps=[
                                    ('imputer', SimpleImputer(strategy='median')),
                                    ('feature_generator', FeatureGenerator(
                                        add_bedrooms_per_room=self.data_transformation_config.add_bedroom_per_room,
                                        columns=numerical_columns)),
                                    ('scaler', StandardScaler())
                                         ]
                                  )
            logging.info(f"Pipeline has been created for numerical columns:{numerical_columns}")
            cat_pipeline= Pipeline(steps=[
                                    ('impute', SimpleImputer(strategy='most_frequent')),
                                    ('one_hot_encoding', OneHotEncoder()),
                                    ('scaler', StandardScaler(with_mean=False))
                                         ]
                                  )
            logging.info(f"Pipeline has been created for categorical columns{categorical_columns}")

            ## Preprocessing steps
            preprocessing= ColumnTransformer([
                                                ('numerical_pipeline', num_pipeline, numerical_columns),
                                                ('categorical_pipeline', cat_pipeline, categorical_columns)
                                             ]
                                            )
            
            return preprocessing

        except Exception as e:
            raise HousingException(e, sys) from e
    def initiate_data_transformation(self, )->DataTransformationArtifact:
        """Transformation of the data is performed by considering pipelines and dataset

        Returns:
            DataTransformationArtifact: Data Transformation artifact details
        """
        try:
            logging.info(f"Getting preprocessing object")
            preprocessing_obj= self.get_transformer_object()
            train_file_path= self.data_ingestion_artifact.train_file_path
            test_file_path= self.data_ingestion_artifact.test_file_path
            schema_file_path= self.data_validation_artifact.schema_file_path

            logging.info(f"loading train and test datasets")
            train_df= load_data(file_path=train_file_path, schema_file_path=schema_file_path)
            test_df= load_data(file_path=test_file_path, schema_file_path=schema_file_path)

            ##Read Schema
            logging.info(f"reading schemas")
            schema= read_yaml_file(schema_file_path)
            target_column_name= schema[TARGET_COLUMN_KEY]

            ### Seggregating input and output features
            input_feature_train_df= train_df.drop(columns=[target_column_name], axis=1)
            target_fearure_train_df= train_df[[target_column_name]]
            input_feature_test_df= test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df= test_df[[target_column_name]]

            ### Transforming the data
            logging.info(f"Transforming train and test datsets using preprocessing object")
            input_feature_train_arr= preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr= preprocessing_obj.transform(input_feature_test_df)

            ###Create train and test arrays by joining both input and output features
            logging.info(f"combining input and output features")
            train_arr= np.c_[input_feature_train_arr, np.array(target_fearure_train_df)]
            test_arr= np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            ### Saving train and test arrays into object
            logging.info(f"Saving the train and test preprocessed arrays into file")
            transformed_train_dir= self.data_transformation_config.transformed_train_dir
            transformed_test_dir= self.data_transformation_config.transformed_test_dir
            train_file_name= os.path.basename(train_file_path).replace(".csv", ".npz")
            test_file_name= os.path.basename(test_file_path).replace(".csv", ".npz")
            transformed_train_file_path=os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path= os.path.join(transformed_test_dir, test_file_name)

            save_numpy_array_data(file_path=transformed_train_file_path,array= train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path,array= test_arr)
            logging.info(f"Saving the preprocessed object")
            preprocessing_obj_file_path= self.data_transformation_config.preprocessed_object_file_path
            save_object(file_path=preprocessing_obj_file_path, obj= preprocessing_obj)
            data_transformation_artifact= DataTransformationArtifact(is_transformed=True,
                                                                        message="Data transformation successfull",
                                                                        transformed_train_file_path=transformed_train_file_path,
                                                                        transformed_test_file_path=transformed_test_file_path,
                                                                        preprocessed_object_file_path=preprocessing_obj_file_path)
            logging.info(f"Data Transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise HousingException(e, sys) from e
