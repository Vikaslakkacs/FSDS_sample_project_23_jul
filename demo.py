from multiprocessing.connection import Pipe
from housing.exception import HousingException
from housing.pipeline.pipeline import Pipeline
import os, sys
from housing.logger import logging
from housing.exception import HousingException

def main():
    try:
        pipeline=Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f"{e}")
        print(e)


if __name__=="__main__":
    main()