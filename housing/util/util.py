import os, sys
import yaml
from housing.exception import HousingException


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
