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

from CommonConstants import *

class WebhookDataGiver(object):

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


    def _find_suitable_uploaded_column(self, uploaded_columns, column_to_find):
        for mycolumn in uploaded_columns:
            if mycolumn == column_to_find:
                return mycolumn
        
        for mycolumn in uploaded_columns:
            if column_to_find in mycolumn:
                return mycolumn
        
        for mycolumn in uploaded_columns:
            if mycolumn in column_to_find:
                return mycolumn
        
        return column_to_find


    def _getJsonDataType1(self, name, label, uploaded_columns):
        myData = {}
        myData["id"] = 0
        myData["name"] = name
        myData["label"] = label
        myData["type"] = 1
        myData["text_value"] = ""
        myData["map_value"] = ""
        myData["list"] = []
        return myData
    
    def _getJsonDataType2(self, name, label, default_value):
        myData = {}
        myData["id"] = 0
        myData["name"] = name
        myData["label"] = label
        myData["type"] = 2
        myData["text_value"] = default_value
        myData["map_value"] = ""
        myData["list"] = self._getJsonDataType4()
        return myData
    

    def _getJsonDataType3(self, name, label, list_elements):
        myData = {}
        myData["id"] = 0
        myData["name"] = name
        myData["label"] = label
        myData["type"] = 3
        myData["text_value"] = ""
        myData["list_value"] = ""
        myData["map_value"] = ""
        myData["list_elements"] = list_elements      
        myData["list"] = self._getJsonDataType4()
        return myData

    def _getJsonDataType4(self):
        myData = {}
        myData["id"] = 0
        myData["text_value"] = ""
        myData["map_value"] = ""
        myData["operation_value"] = ""
        myData["operation_elements"] = ['Append', '+', '-', '*', '/']

        list = []
        list.append(myData)

        return list

    def generateEmptyData(self, locations, accounts) : 
        myData = {}
        myData["id"] = ""
        myData["name"] = ""
        myData["desc"] = ""

        myData["http_method_list"] = ['GET', 'POST']
        myData["http_method"] = "POST"

        myData["url"] = ""
        myData["user"] = ""
        myData["password"] = ""
        myData["token"] = ""
        myData["api_key_name"] = ""
        myData["api_key_value"] = ""
        myData["token"] = ""

        myData["envizi_template_list"] = ['POC', 'ASDL-PMC']
        myData["envizi_template"] = "POC"

        myData["data_template_type_list"] = ['1-single', '2-multiple', '3-multiple-and-common']
        myData["data_template_type"] = "2-multiple"
       
        myData["multiple_records_field"] = ""
    
        fieldsList = self._generateEmptyDataPOC(locations, accounts)
        myData["fields"] = fieldsList

        return myData
    
    def getExcelFilePrefix(self, envizi_template) : 
        filePrefix = FILE_PREFIX_POC_ACCOUNT_SETUP_AND_DATA_LOAD
        if (envizi_template == "ASDL-PMC") :
            filePrefix = FILE_PREFIX_ACCOUNT_SETUP_AND_DATA_LOAD_PMC
        return filePrefix

    def getExcelFileSheetName(self, envizi_template) : 
        sheetName = SHEET_NAME_POC_ACCOUNT_SETUP_AND_DATA_LOAD
        if (envizi_template == "ASDL-PMC") :
            sheetName = SHEET_NAME_ACCOUNT_SETUP_AND_DATA_LOAD_PMC
        return sheetName
    
    def getTemplateColumns(self, envizi_template) : 
        templateName = self.getTemplateFileName(envizi_template)

        template_file_name = os.getenv("DATA_FOLDER", "") + "/templates/" + templateName
        self.logger.info("getTemplateColumns template_file_name ... : " + template_file_name)
        template_columns = self.excelUtil.readColumnName(template_file_name)

        return template_columns


    def getTemplateFileName(self, envizi_template) : 
        templateName = TEMPLATE_POC_ACCOUNT_SETUP_AND_DATA_LOAD
        if (envizi_template == "POC") :
            templateName = TEMPLATE_POC_ACCOUNT_SETUP_AND_DATA_LOAD
        elif (envizi_template == "ASDL-PMC") :
              templateName = TEMPLATE_ACCOUNT_SETUP_AND_DATA_LOAD_PMC
        return templateName


    def populateFields(self, payload, locations, accounts) : 
        
        envizi_template = payload["envizi_template"]
        fieldsList = []
        if (envizi_template == "POC") :
            fieldsList = self._generateEmptyDataPOC(locations, accounts)
        elif (envizi_template == "ASDL-PMC") :
             fieldsList = self._generateEmptyDataASDLPMC(locations, accounts)
        else  :
             payload["envizi_template"] = "POC"
             fieldsList = self._generateEmptyDataPOC(locations, accounts)

        payload["fields"] = fieldsList


    def _generateEmptyDataPOC(self, locations, accounts) : 
        uploaded_columns = ['']

        fieldsList = []
        fieldsList.append(self._getJsonDataType1('organization', 'Organization', uploaded_columns))
        fieldsList.append(self._getJsonDataType3('location', 'Location', uploaded_columns, locations))
        fieldsList.append(self._getJsonDataType2('account_style', 'Account Style Caption',"", uploaded_columns))
        fieldsList.append(self._getJsonDataType3('account_name', 'Account Number', uploaded_columns, accounts))
        fieldsList.append(self._getJsonDataType2('account_ref', 'Account Reference', "", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('account_supplier', 'Account Supplier', "", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('record_start', 'Record Start YYYY-MM-DD', "2024-01-01",uploaded_columns))
        fieldsList.append(self._getJsonDataType2('record_end', 'Record End YYYY-MM-DD', "2024-01-01", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('quantity', 'Quantity', "", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('total_cost', 'Total cost (incl. Tax) in local currency', "", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('record_reference', 'Record Reference', "", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('record_invoice_number', 'Record Invoice Number', "", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('record_data_quality', 'Record Data Quality', "", uploaded_columns))

        return fieldsList

    def _generateEmptyDataASDLPMC(self, locations, accounts) : 
        uploaded_columns = ['']

        fieldsList = []
        fieldsList.append(self._getJsonDataType1('organization_link', 'Organization Link', uploaded_columns))
        fieldsList.append(self._getJsonDataType1('organization', 'Organization', uploaded_columns))
        fieldsList.append(self._getJsonDataType3('location', 'Location', uploaded_columns, locations))
        fieldsList.append(self._getJsonDataType2('location_ref', 'Location Ref',"", uploaded_columns))

        fieldsList.append(self._getJsonDataType2('account_style_link', 'Account Style Link',"", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('account_style', 'Account Style Caption',"", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('account_subtype', 'Account Subtype',"", uploaded_columns))

        fieldsList.append(self._getJsonDataType3('account_name', 'Account Number', uploaded_columns, accounts))
        fieldsList.append(self._getJsonDataType2('account_ref', 'Account Reference', "", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('account_supplier', 'Account Supplier', "", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('account_reader', 'Account Reader', "", uploaded_columns))


        fieldsList.append(self._getJsonDataType2('record_start', 'Record Start YYYY-MM-DD', "2024-01-01",uploaded_columns))
        fieldsList.append(self._getJsonDataType2('record_end', 'Record End YYYY-MM-DD', "2024-01-01", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('record_data_quality', 'Record Data Quality', "", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('record_billing_type', 'Record Billing Type', "", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('record_subtype', 'Record Subtype', "", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('record_entry_method', 'Record Entry Method', "", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('record_reference', 'Record Reference', "", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('record_invoice_number', 'Record Invoice Number', "", uploaded_columns))

        fieldsList.append(self._getJsonDataType2('quantity', 'Quantity', "", uploaded_columns))
        fieldsList.append(self._getJsonDataType2('total_cost', 'Total Cost', "", uploaded_columns))

        return fieldsList