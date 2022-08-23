import os, sys
from tkinter import E
import yaml
from housing.exception import HousingException
import numpy as np
import dill
import pandas as pd
from housing.constant import *
def read_yaml_file(file_path:str)->dict:
    """reads YAML file with package yaml

    Args:
        file_path (str): file path where yaml is present

    Returns:
        dict: with key value pairs for each segment
    """
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise HousingException(e, sys) from e


def load_data(file_path:str, schema_file_path:str) -> pd.DataFrame:
    """Changing the type cast of the features according to schema file

    Args:
        file_path (str): _description_
        schema_file_path (str): schema file path where all the type cast details of features are available

    Returns:
        pd.DataFrame: dataset with corrected type cast of features to make transformation
    """
    try:
        dataset_schema= read_yaml_file(schema_file_path)
        schema= dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]

        ##Get the data frame
        dataframe= pd.read_csv(file_path)

        error_message= ""

        ### loop around the columns and change the data types
        for column in dataframe.columns:
            if column in list(schema.keys()):

                dataframe[column].astype(schema[column])
            else:
                error_message= f"{error_message} \nColumn: {column} is not in schema."
                raise Exception(error_message)
        return dataframe
        
    except Exception as e:
        raise HousingException(e, sys) from e


def save_numpy_array_data(file_path:str, array:np.array):
    """Saves Numpy array data to file

    Args:
        file_path (str): location to store the file
        array (np.array): array data to save
    """
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        raise HousingException(e, sys) from e

def load_numpy_array_data(file_path:str) -> np.array:
    """Load Numpy array data from file

    Args:
        file_path (str): file path where file object is stored

    Raises:
        HousingException: Loading un successfull

    Returns:
        np.array: Numpy array of loaded data
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
        
    except Exception as e:
        raise HousingException(e, sys) from e

def save_object(file_path:str, obj):
    """Saving object using dill library

    Args:
        file_name (str): string
        obj (_type_): any object
    """
    try:
        dir_path= os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise HousingException(e, sys) from e

def load_object(file_path:str):
    """Loading file object from file to system

    Args:
        file_path (str): file path where object is stored
    """
    try:
        with open(file_path, 'rb') as file_obj:
            dill.load(file_obj)
    except Exception as e:
        raise HousingException(e, sys) from e