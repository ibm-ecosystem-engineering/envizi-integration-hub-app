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


    def _getJsonDataType1(self, name, label):
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
        myData["firewall_url"] = ""
        myData["firewall_user"] = ""
        myData["firewall_password"] = ""

        myData["envizi_template_list"] = ['POC', 'ASDL-PMC']
        myData["envizi_template"] = "POC"

        myData["data_template_type_list"] = ['1-single', '2-multiple', '3-multiple-and-common']
        myData["data_template_type"] = "2-multiple"
       
        myData["multiple_records_field"] = ""
    
        fieldsList = self._generateEmptyDataPOC(locations, accounts)
        myData["fields"] = fieldsList

        return myData
    

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

        fieldsList = []
        fieldsList.append(self._getJsonDataType1('organization', 'Organization'))
        fieldsList.append(self._getJsonDataType3('location', 'Location', locations))
        fieldsList.append(self._getJsonDataType2('account_style', 'Account Style Caption',""))
        fieldsList.append(self._getJsonDataType3('account_name', 'Account Number', accounts))
        fieldsList.append(self._getJsonDataType2('account_ref', 'Account Reference', ""))
        fieldsList.append(self._getJsonDataType2('account_supplier', 'Account Supplier', ""))
        fieldsList.append(self._getJsonDataType2('record_start', 'Record Start YYYY-MM-DD', "2024-01-01"))
        fieldsList.append(self._getJsonDataType2('record_end', 'Record End YYYY-MM-DD', "2024-01-01"))
        fieldsList.append(self._getJsonDataType2('quantity', 'Quantity', ""))
        fieldsList.append(self._getJsonDataType2('total_cost', 'Total cost (incl. Tax) in local currency', ""))
        fieldsList.append(self._getJsonDataType2('record_reference', 'Record Reference', ""))
        fieldsList.append(self._getJsonDataType2('record_invoice_number', 'Record Invoice Number', ""))
        fieldsList.append(self._getJsonDataType2('record_data_quality', 'Record Data Quality', ""))

        return fieldsList

    def _generateEmptyDataASDLPMC(self, locations, accounts) : 
        fieldsList = []
        fieldsList.append(self._getJsonDataType1('organization_link', 'Organization Link'))
        fieldsList.append(self._getJsonDataType1('organization', 'Organization'))
        fieldsList.append(self._getJsonDataType3('location', 'Location', locations))

        fieldsList.append(self._getJsonDataType2('location_ref', 'Location Ref',""))

        fieldsList.append(self._getJsonDataType2('account_style_link', 'Account Style Link',""))
        fieldsList.append(self._getJsonDataType2('account_style', 'Account Style Caption',""))
        fieldsList.append(self._getJsonDataType2('account_subtype', 'Account Subtype',""))

        fieldsList.append(self._getJsonDataType3('account_name', 'Account Number', accounts))
        fieldsList.append(self._getJsonDataType2('account_ref', 'Account Reference', ""))
        fieldsList.append(self._getJsonDataType2('account_supplier', 'Account Supplier', ""))
        fieldsList.append(self._getJsonDataType2('account_reader', 'Account Reader', ""))


        fieldsList.append(self._getJsonDataType2('record_start', 'Record Start YYYY-MM-DD', "2024-01-01"))
        fieldsList.append(self._getJsonDataType2('record_end', 'Record End YYYY-MM-DD', "2024-01-01"))
        fieldsList.append(self._getJsonDataType2('record_data_quality', 'Record Data Quality', ""))
        fieldsList.append(self._getJsonDataType2('record_billing_type', 'Record Billing Type', ""))
        fieldsList.append(self._getJsonDataType2('record_subtype', 'Record Subtype', ""))
        fieldsList.append(self._getJsonDataType2('record_entry_method', 'Record Entry Method', ""))
        fieldsList.append(self._getJsonDataType2('record_reference', 'Record Reference', ""))
        fieldsList.append(self._getJsonDataType2('record_invoice_number', 'Record Invoice Number', ""))

        fieldsList.append(self._getJsonDataType2('quantity', 'Quantity', ""))
        fieldsList.append(self._getJsonDataType2('total_cost', 'Total Cost', ""))

        return fieldsList