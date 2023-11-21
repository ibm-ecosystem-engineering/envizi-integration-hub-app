from datetime import datetime, timedelta
import logging
import os


### Static methods
class MathUtil :
    logger = logging.getLogger('MathUtil')
    logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    @staticmethod
    def divide(num1, num2):
        result = 0
        try:
            result = num1 / num2
        except Exception as e:
            MathUtil.logger.debug(f' Error in divide : {e} ')
        return result

