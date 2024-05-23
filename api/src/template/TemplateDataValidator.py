import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

import logging 
import os, json

from util.DateUtils import DateUtils
from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.DictionaryUtil import DictionaryUtil
from util.ExcelUtil import ExcelUtil
from util.NumberUtil import NumberUtil

from CommonConstants import *

class TemplateDataValidator(object):

    def __init__(
        self,
        fileUtil: FileUtil,
        configUtil: ConfigUtil
    ) -> None:
        self.fileUtil = fileUtil
        self.configUtil = configUtil
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())
        self.excelUtil = ExcelUtil()

    def validateData(self, columnLabel, columnValue, locations, account_styles) : 
        result = None

        if (columnLabel == 'Organization') :
            result = self._validateData_2_equal(columnLabel, columnValue, self.configUtil.ENVIZI_ORG_NAME)
        elif (columnLabel == 'Location') :
            result = self._validateData_3_in_list(columnLabel, columnValue, locations)
        elif (columnLabel == 'Account Style Caption') :
            result = self._validateData_3_in_list(columnLabel, columnValue, account_styles)
        elif (columnLabel == 'Account Number') :
            result = self._validateData_1_empty(columnLabel, columnValue)
        elif (columnLabel == 'Record Start YYYY-MM-DD') :
            result = self._validateData_4_date(columnLabel, columnValue)
        elif (columnLabel == 'Record End YYYY-MM-DD') :
            result = self._validateData_4_date(columnLabel, columnValue)
        elif (columnLabel == 'Quantity') :
            result = self._validateData_5_non_empty_number(columnLabel, columnValue)
        elif (columnLabel == 'Total cost (incl. Tax) in local currency') :
            result = self._validateData_6_empty_or_number(columnLabel, columnValue)
        
        elif (columnLabel == 'Organization Link') :
            result = self._validateData_2_equal(columnLabel, columnValue, self.configUtil.ENVIZI_ORG_LINK)

        elif (columnLabel == 'Account Style Link') :
            result = self._validateData_1_empty(columnLabel, columnValue)

        self.logger.info("TemplateDataValidator validateData ... : " + str(result))

        return result


    ### Value should be equaivalent to given value
    def _validateData_1_empty(self, columnLabel, columnValue) : 
        result = None
        if (not columnValue) :
            result = "The value of the " + columnLabel + " should not be empty"
        return result 

    ### Value should be equaivalent to given value
    def _validateData_2_equal(self, columnLabel, columnValue, compareValue) : 
        result = None
        if (str(columnValue) != str(compareValue)) :
            result = "The value of the " + columnLabel + " should be " + str(compareValue)
        return result 

    ### Value should not be empty
    ### Value should be in the inside the given list (if list is empty then check is not required)
    def _validateData_3_in_list(self, columnLabel, columnValue, compareValueList) : 
        result = None
        if (not columnValue) :
            result = "The value of the " + columnLabel + " should not be empty"
        elif compareValueList and len(compareValueList) > 1:
            if (columnValue not in compareValueList) :
                result = "The value of the " + columnLabel + " doesn't exists in Envizi"
        return result 
    
    ### Value should be of the format YYYY-MM-DD
    def _validateData_4_date(self, columnLabel, columnValue) : 
        result = None
        if not DateUtils.is_valid_date_YYYY_MM_DD(columnValue) :
            result = "The value of the " + columnLabel + " should be in the format YYYY-MM-DD"
        return result

    ### Should be non empty
    ### Should be number
    def _validateData_5_non_empty_number(self, columnLabel, columnValue) : 
        result = None
        if not NumberUtil.isNumber(columnValue) :
            result = "The value of the " + columnLabel + " should be a valid number"
        return result

    ### Can be empty, 
    ### if non-empty then it should be number
    def _validateData_6_empty_or_number(self, columnLabel, columnValue) : 
        result = None
        if (columnValue) :
            if not NumberUtil.isNumber(columnValue) :
                result = "The value of the " + columnLabel + " should be a valid number"
        return result