from datetime import datetime, timedelta
import logging
import os

### Static methods
class DateUtils :
    
    logger = logging.getLogger('DateUtil')
    logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    @staticmethod
    def getCurrentDateString():
        current_date = datetime.now() 
        date_time = current_date.strftime("%Y-%m-%d")
        # print(f"getCurrentDateString : {date_time}")
        return date_time

    def getCurrentDateTimeString():
        current_date = datetime.now() 
        date_time = current_date.strftime("%Y-%m-%d-%H%M%S-%f")
        # print(f"getCurrentDateTimeString : {date_time}")
        return date_time
    
    @staticmethod
    def validateDate():
        return DateUtils.getCurrentDateString()

    @staticmethod
    def stringToDate(dateString):
        result = datetime.now() 
        try:
            result = datetime.strptime(dateString, "%Y-%m-%d")
        except Exception as e:
            DateUtils.logger.debug(f' Error in covertToDate : {e} ')
        return result
    
    @staticmethod
    def dateToString(dateObject):
        result = ""
        try:
            result = dateObject.strftime('%Y-%m-%d')
        except Exception as e:
            DateUtils.logger.debug(f' Error in dateToString : {e} ')
        return result

