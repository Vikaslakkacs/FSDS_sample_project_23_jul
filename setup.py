from gettext import find
from setuptools import setup, find_packages
from typing import List 

### Declaring variables for setup function.
PROJECT_NAME="housing-predictor"
VERSION="0.0.1"
AUTHOR="Vikas Lakka"
DESCRIPTION="First Machine learning project"
PACKAGES=['housing']
REQUIREMENTS_FILENAME="requirements.txt"

def get_requirements_list()->List[str]:
    """
    Description: This function will return list of requirements available in requirements.txt file

    Returns:
        List[str]: list of packages available in requirements.txt file.
    """
    with open("requirements.txt","r",) as requirements_file:
        return requirements_file.readlines().remove("-e .")



setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(), # it will return the packages whereever the folder has __init__.py file in it
                              # here it will pick 'housing'
    install_requires=get_requirements_list()# What external libraries that require(requirements.txt)

)
