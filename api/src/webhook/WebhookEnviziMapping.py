import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

import logging 
import os, json

from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.DictionaryUtil import DictionaryUtil
from util.JsonUtil import JsonUtil
from util.ExcelUtil import ExcelUtil
from util.MathUtil import MathUtil
from CommonConstants import *
from excelpro.ExcelProDataValidator import ExcelProDataValidator

class WebhookEnviziMapping(object):

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
        self._init_config()
        self.excelProDataValidator = ExcelProDataValidator(self.fileUtil, self.configUtil)

    def _init_config(self):
        self.DATA_STORE_FOLDER = os.getenv("DATA_STORE_FOLDER") 
        self.WEBHOOK_FOLDER = self.DATA_STORE_FOLDER + "/webhook/"
        self.WEBHOOK_FILE = self.WEBHOOK_FOLDER + "/webhook.json"
        self.excelUtil = ExcelUtil()

    def map_webhook_data_to_envizi_format(self, webhook_detail_data, webhook_execute_response, template_columns) : 
        mappingFieldsArray = webhook_detail_data["fields"]
        data_template_type = webhook_detail_data["data_template_type"]

        resp = {}
        if (data_template_type == "1-single") :
            resp = self._map_webhook_type_1(webhook_execute_response, mappingFieldsArray, template_columns)
        elif (data_template_type == "2-multiple") :
            resp = self._map_webhook_type_2(webhook_execute_response, mappingFieldsArray, template_columns)
        elif (data_template_type == "3-multiple-and-common") :
            ### Get mutliple records data field
            multiple_records_field = DictionaryUtil.getValue_key1(webhook_detail_data, "multiple_records_field", "")
            multiple_records_field_data = DictionaryUtil.findValue(webhook_execute_response, multiple_records_field)            

            resp = self._map_webhook_type_3(webhook_execute_response, mappingFieldsArray, template_columns, multiple_records_field_data)

        return resp

    def _map_webhook_type_1(self, webhook_data, mappingFieldsArray, template_columns):
        self.logger.info("map_webhook_type_1  ... ")

        resp = {}
        resp["processed_data"] = []
        resp["validation_errors"] = []
        result = self._map_webhook_type_common (webhook_data, None, mappingFieldsArray, template_columns)
        resp["processed_data"] .append(result["processed_row"])
        resp["validation_errors"] .append(result["validation_errors"])

        return resp


    def _map_webhook_type_2(self, webhook_data, mappingFieldsArray, template_columns):
        self.logger.info("map_webhook_type_2  ... ")

        resp = {}
        resp["processed_data"] = []
        resp["validation_errors"] = []
        for webhook_row_data in webhook_data :
            result = self._map_webhook_type_common (webhook_data, webhook_row_data, mappingFieldsArray, template_columns)
            resp["processed_data"] .append(result["processed_row"])
            resp["validation_errors"] .append(result["validation_errors"])

        return resp


    def _map_webhook_type_3(self, webhook_data, mappingFieldsArray, template_columns, multiple_records_field_data):
        self.logger.info("map_webhook_type_3  ... ")

        resp = {}
        resp["processed_data"] = []
        resp["validation_errors"] = []

        for webhook_row_data in multiple_records_field_data :
            result = self._map_webhook_type_common (webhook_data, webhook_row_data, mappingFieldsArray, template_columns)
            resp["processed_data"] .append(result["processed_row"])
            resp["validation_errors"] .append(result["validation_errors"])

        return resp


    def _map_webhook_type_common(self, webhook_data, webhook_row_data, mappingFieldsArray, template_columns):
        self.logger.info("map_webhook_type_common  ... ")

        validation_errors = []
        processed_row = {}

        for template_column_label in template_columns:
            
            mappingField = JsonUtil.findElement(mappingFieldsArray, "label", template_column_label)
            
            ### Process Value
            processed_value = self._processFieldValue(webhook_data, webhook_row_data, mappingField)
            processed_row[template_column_label] = processed_value

            ### Process Validation
            errorText = self.excelProDataValidator.validateData(0, template_column_label , processed_value, [], [], [])
            if errorText :
                validation_errors.append(errorText)

        resp = {}
        resp["processed_row"] = processed_row
        resp["validation_errors"] = validation_errors

        return resp


    def _processFieldValue(self, webhook_data, webhook_row_data, mappingField) : 
        item = mappingField
        map_value = item["map_value"]
        text_value = item["text_value"]
        list_value = DictionaryUtil.getValue_key1(item, "list_value", "")
        subItemList = item["list"] 
        result = ""
        
        self.logger.info(f"_processFieldValue text_value : {text_value}, map_value : {map_value}")

        if (text_value != "") :
            result = text_value
        elif (list_value != "") :
            result = list_value
        elif (map_value != "") :
            result = self._processMapValue(webhook_data, webhook_row_data, map_value)
        else :
            firstRecord = True
            operation_value_prev = ""
            for subItem in subItemList :
                text_value = subItem["text_value"]
                map_value = subItem["map_value"]
                list_value = DictionaryUtil.getValue_key1(subItem, "list_value", "")
                operation_value = DictionaryUtil.getValue_key1(subItem, "operation_value", "")

                curr_value = ""
                if (text_value != "") :
                    curr_value = text_value
                elif (list_value != "") :
                    curr_value = list_value
                elif (map_value != "") :
                    curr_value = self._processMapValue(webhook_data, webhook_row_data, map_value)

                if (firstRecord) :
                    firstRecord = False
                    result = curr_value
                else :
                    if (operation_value_prev == "Append") :
                        result = str(result) + str(curr_value)
                    elif (operation_value_prev == "+") :
                        result = MathUtil.add_or_append(result, curr_value) 
                    elif (operation_value_prev == "-") :
                        result = MathUtil.sub_or_append(result, curr_value) 
                    elif (operation_value_prev == "*") :
                        result = MathUtil.mul_or_append(result, curr_value) 
                    elif (operation_value_prev == "/") :
                        result = MathUtil.divide_or_append(result, curr_value) 
                    else :
                        result = str(result) + str(curr_value)

                operation_value_prev = operation_value



    def _processMapValue(self, webhook_data, webhook_row_data, mapValue) : 
        resultValue = None
        ### If row_data is not empty..then try in row_data first
        if (webhook_row_data != None) :
            resultValue = DictionaryUtil.findValue(webhook_row_data, mapValue)

        ### If returned data is empty from the previous try, then try in webhook_data
        if (resultValue == None) :
            resultValue = DictionaryUtil.findValue(webhook_data, mapValue)

        return resultValue
