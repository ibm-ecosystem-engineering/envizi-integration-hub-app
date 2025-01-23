from datetime import datetime, timedelta
import logging
import os


### Static methods
class StringUtil :
    logger = logging.getLogger('StringUtil')
    logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    @staticmethod
    def boolean_to_text(booleanValue):
        result = "False"
        if (booleanValue) :
            result = "True"
        return result