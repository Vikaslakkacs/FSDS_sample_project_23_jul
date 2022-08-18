import os, sys
from tkinter import E
import yaml
from housing.exception import HousingException
import numpy as np
import dill

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