from setuptools import setup
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
        return requirements_file.readlines()



setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=PACKAGES,
    install_requires=get_requirements_list()

)
