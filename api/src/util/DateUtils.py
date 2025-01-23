from datetime import datetime, timedelta
import pandas as pd
import logging
import os
import re
from dateutil import parser

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
    
    def getSimpleCurrentDateTimeString():
        current_date = datetime.now() 
        date_time = current_date.strftime("%Y%m%d%H%M%S")
        return date_time
    
    def getCurrentDateTimeString2():
        current_date = datetime.now() 
        date_time = current_date.strftime("%Y-%m-%d %H:%M:%S")
        return date_time

    @staticmethod
    def getNextYearDateString():
        current_date = datetime.now() 
        try:
            next_year_same_date = current_date.replace(year=current_date.year + 1)
        except ValueError:
            # Handle February 29th for leap years
            next_year_same_date = current_date + timedelta(days=365)
        date_time = next_year_same_date.strftime("%Y-%m-%d")
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


    @staticmethod
    def timeStampToDateString(timestamp : pd.Timestamp):
        result = datetime.now() 
        try:
            # Convert timestamp to datetime object
            # dt_object = datetime.utcfromtimestamp(timestamp)

            # Format datetime object into YYYY-MM-DD format
            result = timestamp.strftime("%Y-%m-%d")
        except Exception as e:
            DateUtils.logger.debug(f' Error in timeStampToDateString : {e} ')
        return result
    
    @staticmethod
    def convertDateFormatYYYYMMDD(date_string):
        result = ""
        try:
            input_format = "%d-%b-%y"
            output_format = "%Y-%m-%d"
            parsed_date = datetime.strptime(date_string, input_format)
            result = parsed_date.strftime(output_format)
        except Exception as e:
            DateUtils.logger.debug(f' Error in covertDateFormat1 : {e} ')
        return result    
    
    @staticmethod
    def is_valid_date_YYYY_MM_DD(date_string):
        result = False
        try:
            # Define a regex pattern for YYYY-MM-DD format
            pattern = r'^\d{4}-\d{2}-\d{2}$'
            
            # Use the match function to check if the date string matches the pattern
            if re.match(pattern, date_string):
                result = True
        except Exception as e:
            result = False
        return result
    
    @staticmethod
    def convert_any_date_format_to_YYYYMMDD(date_string):
        result = date_string
        try:
            # Automatically parse the date string into a datetime object
            parsed_date = parser.parse(date_string)
            # Format the datetime object into "YYYY-MM-DD"
            result = parsed_date.strftime("%Y-%m-%d")
        except Exception as e:
            DateUtils.logger.debug(f' Error in convert_any_date_format_to_YYYYMMDD : {e} ')
        
        return result