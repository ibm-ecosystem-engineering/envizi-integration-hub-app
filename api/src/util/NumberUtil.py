from datetime import datetime, timedelta
import logging
import os


### Static methods
class NumberUtil :
    logger = logging.getLogger('NumberUtil')
    logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    @staticmethod
    def isNumber(num1):
        result = False
        try:
            int(num1)
            result = True
        except Exception as e:
            NumberUtil.logger.debug(f' Error in isNumber : {e} ')
            result = False

        return result

    @staticmethod
    def stingToInt(stringValue, defaultValue):
        result = defaultValue
        try:
            result = int(stringValue)
        except Exception as e:
             result = defaultValue

        return result
