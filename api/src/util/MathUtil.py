from datetime import datetime, timedelta
import logging
import os


### Static methods
class MathUtil :
    logger = logging.getLogger('MathUtil')
    logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    @staticmethod
    def add_or_append(num1, num2):
        result = 0
        try:
            result = int(num1) + int(num2)
        except Exception as e:
            MathUtil.logger.error(f' Error in add_or_append :{num1}:{num2}: {e} ')
            try:
                result = str(num1) + str(num2)
            except Exception as e:
                MathUtil.logger.error(f' Error in add_or_append :{num1}:{num2}: {e} ')

        return result

    @staticmethod
    def sub_or_append(num1, num2):
        result = 0
        try:
            result = int(num1) - int(num2)
        except Exception as e:
            MathUtil.logger.debug(f' Error in sub_or_append : {e} ')
            try:
                result = str(num1) + str(num2)
            except Exception as e:
                MathUtil.logger.debug(f' Error in sub_or_append : {e} ')
        return result

    @staticmethod
    def mul_or_append(num1, num2):
        result = 0
        try:
            result = int(num1) * int(num2)
        except Exception as e:
            MathUtil.logger.debug(f' Error in mul_or_append : {e} ')
            try:
                result = str(num1) + str(num2)
            except Exception as e:
                MathUtil.logger.debug(f' Error in mul_or_append : {e} ')
        return result

    @staticmethod
    def divide_or_append(num1, num2):
        result = 0
        try:
            result = int(num1) / int(num2)
        except Exception as e:
            MathUtil.logger.debug(f' Error in divide_or_append : {e} ')
            try:
                result = str(num1) + str(num2)
            except Exception as e:
                MathUtil.logger.debug(f' Error in divide_or_append : {e} ')
        return result

    @staticmethod
    def divide(num1, num2):
        result = 0
        try:
            result = int(num1) / int(num2)
        except Exception as e:
            MathUtil.logger.debug(f' Error in divide : {e} ')
        return result
