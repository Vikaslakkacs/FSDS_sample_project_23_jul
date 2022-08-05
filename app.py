'''from flask import Flask, app
from housing.logger import logging
from housing.exception import HousingException
import sys
app=Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    try:
        raise Exception("Exception raised for testing")
    except Exception as e:
        housing= HousingException(e,sys)
        logging.info("Exception testing")
        logging.info(housing.error_message)
        logging.info("Testing logging module.")
        ##raise HousingException(e, sys) from e
    return "CI/CD pipe line has successfully completed"

if __name__=="__main__":
    app.run(debug=True)
    '''
from housing.config.configuration import Configuration

if __name__=="__main__":
    config= Configuration() 
    print(config.model_trainer_config)