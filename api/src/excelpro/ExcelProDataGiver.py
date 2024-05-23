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
from util.MathUtil import MathUtil

from CommonConstants import *

class ExcelProDataGiver(object):

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
        myData["uploaded_column"] = self._find_suitable_uploaded_column(uploaded_columns, label)      
        myData["list"] = []
        return myData
    
    def _getJsonDataType2(self, name, label, default_value, uploaded_columns):
        myData = {}
        myData["id"] = 0
        myData["name"] = name
        myData["label"] = label
        myData["type"] = 2
        myData["text_value"] = default_value
        myData["uploaded_column"] = self._find_suitable_uploaded_column(uploaded_columns, label)      
        myData["list"] = self._getJsonDataType4()
        return myData
    

    def _getJsonDataType3(self, name, label, uploaded_columns, list_elements):
        myData = {}
        myData["id"] = 0
        myData["name"] = name
        myData["label"] = label
        myData["type"] = 3
        myData["text_value"] = ""
        myData["list_value"] = ""
        myData["uploaded_column"] = self._find_suitable_uploaded_column(uploaded_columns, label)      
        myData["list_elements"] = list_elements      
        myData["list"] = self._getJsonDataType4()
        return myData

    def _getJsonDataType4(self):
        myData = {}
        myData["id"] = 0
        myData["text_value"] = ""
        myData["uploaded_column"] = ""
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
        myData["envizi_template_list"] = ['POC', 'ASDL-PMC']
        myData["envizi_template"] = "POC"
       
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
    
    def obtainValueForColumn (self, fields, excelRow, template_column_text):
        result = ""

        for field_data in fields:
            field_label = field_data["label"]
            if (field_label == template_column_text) :
                text_value = field_data["text_value"]
                list_value = DictionaryUtil.getValue_key1(field_data, "list_value", "")
                uploaded_column = field_data["uploaded_column"]

                if (text_value != "") :
                    result = text_value
                    break
                elif (list_value != "") :
                    result = list_value
                    break
                elif (uploaded_column != "") :
                    result = self.excelUtil.getColumnValue(excelRow, uploaded_column)
                    break
                else :
                    firstRecord = True
                    operation_value_prev = ""
                    for subItem in field_data["list"] :
                        text_value = subItem["text_value"]
                        uploaded_column = subItem["uploaded_column"]
                        operation_value = subItem["operation_value"]

                        curr_value = ""
                        if (text_value != "") :
                            curr_value = text_value
                        elif (list_value != "") :
                            curr_value = list_value
                        elif (uploaded_column != "") :
                            # curr_value = excelRow.loc[uploaded_column]
                            curr_value = self.excelUtil.getColumnValue(excelRow, uploaded_column)

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

        return result
