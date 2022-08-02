import os
import sys

class HousingException(Exception):
    
    
    def __init__(self, error_message:Exception, error_details:sys):
        ## Pass information to parent class Exception
        super().__init__(error_message)## == Exception(error_message)
        self.error_message=HousingException.get_detailed_error_message(error_message=error_message,
                                                                        error_details=error_details)

    @staticmethod
    def get_detailed_error_message(error_message:Exception, error_details:sys)-> str:
        ### Returns tuple with traceback string
        _, _, exeception_traceback= error_details.exc_info()
        line_number= exeception_traceback.tb_frame.f_lineno
        file_name= exeception_traceback.tb_frame.f_code.co_filename

        error_message= f"Error occurred in script:[{file_name}] at line number: [{line_number}] error message: [{error_message}]"
        return error_message
    
    ## Error message
    ## Whenever we use class in print statement it will pring __str__ value
    def __str__(self):
        return self.error_message
    ### when ever we create class in variable it will represent __repr__ value
    def __repr__(self)-> str:
        return HousingException.__name__.str()