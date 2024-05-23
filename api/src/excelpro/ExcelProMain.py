import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

from typing import Dict, Optional, Any, Iterable, List
import uuid
import pandas as pd

# import getpass
import logging 
import os, json

from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.DictionaryUtil import DictionaryUtil
from util.ApiUtil import ApiUtil
from util.ExcelUtil import ExcelUtil
from excel.ExcelProcessor import ExcelProcessor
from excelpro.ExcelProDB import ExcelProDB
from excelpro.ExcelProS3 import ExcelProS3
from excelpro.ExcelProRun import ExcelProRun
from excelpro.ExcelProDataGiver import ExcelProDataGiver
from template.TemplateDataValidator import TemplateDataValidator
from template.TemplateMain import TemplateMain

from envizi.EnviziMain import EnviziMain

from CommonConstants import *
from util.DateUtils import DateUtils

class ExcelProMain(object):

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

    def _init_config(self):
        self.LOAD_ENVIZI_DATA = os.getenv("LOAD_ENVIZI_DATA") 
        self.DATA_STORE_FOLDER = os.getenv("DATA_STORE_FOLDER") 
        self.EXCELPRO_FOLDER = self.DATA_STORE_FOLDER + "/excelpro/"
        self.EXCELPRO_FILE = self.EXCELPRO_FOLDER + "/excelpro.json"
        self.excelUtil = ExcelUtil()
        self.excelProcessor = ExcelProcessor(self.fileUtil, self.configUtil)
        self.excelproDB = ExcelProDB(self.fileUtil, self.configUtil)
        self.excelproS3 = ExcelProS3(self.fileUtil, self.configUtil)
        self.excelproRun = ExcelProRun(self.fileUtil, self.configUtil)
        self.excelProDataGiver = ExcelProDataGiver(self.fileUtil, self.configUtil)
        self.enviziMain = EnviziMain(self.fileUtil, self.configUtil)
        self.templateMain = TemplateMain(self.fileUtil, self.configUtil)
        self.templateDataValidator = TemplateDataValidator(self.fileUtil, self.configUtil)

    def loadAll(self):
        self.logger.info("loadExcelPros  ... ")

        data = self.fileUtil.loadJsonFileContent(self.EXCELPRO_FILE)

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("excelpro.json", json.dumps(data))

        resp = {
            "msg": "Records are loaded successfully",
            "data": data,
        }

        return resp
    
    def loadExcelPro(self, payload):
        self.logger.info("loadExcelPro  ... ")
        self.logger.info("loadExcelPro : " + json.dumps(payload))

        ### Retrieve excelpro details from DB (file)
        id = payload["id"]
        excelpro_detail_data = self.excelproDB.loadExcelProDetailById(id)

        resp = {
            "msg": "Record is loaded successfully",
            "data": excelpro_detail_data,
        }

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("excelpro.json", json.dumps(resp))

        return resp
    
    def loadExcelProNew(self, payload):
        self.logger.info("loadExcelProNew  ... ")
        self.logger.info("loadExcelProNew : " + json.dumps(payload))

        ### Retrive locations and accounts
        locations = []
        accounts = []
        if (self.LOAD_ENVIZI_DATA == "TRUE") : 
            list  = self.enviziMain.exportLocation()
            locations = list["data"]
            list = self.enviziMain.exportAccounts()
            accounts = list["data"]

        ### Generate Empty Data
        excelpro_detail_data = self.excelProDataGiver.generateEmptyData(locations, accounts)

        resp = {
            "msg": "Record is loaded successfully",
            "data": excelpro_detail_data,
        }

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("excelpro.json", json.dumps(resp))

        return resp


    def loadExcelProTemplateChange(self, payload):
        self.logger.info("loadExcelProTemplateChange  ... ")
        self.logger.info("loadExcelProTemplateChange : " + json.dumps(payload))

        ### Retrive locations and accounts
        locations = []
        accounts = []
        if (self.LOAD_ENVIZI_DATA == "TRUE") : 
            list  = self.enviziMain.exportLocation()
            locations = list["data"]
            list = self.enviziMain.exportAccounts()
            accounts = list["data"]

        ### Generate fields based on template
        self.excelProDataGiver.populateFields(payload, locations, accounts)

        resp = {
            "msg": "Record is loaded successfully",
            "data": payload,
        }

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("excelpro.json", json.dumps(resp))

        return resp
    
    def saveExcelPro(self, payload):
        self.logger.info("saveExcelPro  ... ")

        ### Save excelpro master
        id = self.excelproDB.saveExcelProMaster(payload)
        payload["id"] = id

        ### Save excelpro detail
        result = self.excelproDB.saveExcelProDetail(payload)

        resp = {
            "msg": "Record is saved successfully",
            "data": result,
        }
        return resp
    
    def deleteExcelPro(self, payload):
        self.logger.info("deleteExcelPro  ... ")
        result = self.excelproDB.deleteExcelPro(payload)
        resp = {
            "msg": "Record is deleted successfully",
            "data": result
        }
        return resp


    def uploadData (self, file, envizi_template):

        ## Save the file
        fileName = file.filename
        self.logger.info("uploadData uploaded fileName ... : " + fileName)
        fileNameWithPath = self.fileUtil.getFileNameWithoutCounter(fileName)
        file.save(fileNameWithPath)

        template_columns = self.templateMain.getTemplateColumns(envizi_template)

        ### Source
        list = self.excelUtil.readColumnName(fileNameWithPath)
        uploaded_columns = ['']
        for item in list:
            self.logger.info("uploadData template_file_name item :" + item + ":")
            if (item != "") :
                uploaded_columns.append(item)

        resp = {
                "uploaded_columns": uploaded_columns,
                "template_columns": template_columns,
                "uploadedFile": fileNameWithPath,
                "msg": "The columns of the " + fileName + " file have been successfully loaded"
                }

        self.fileUtil.writeInFileWithCounter("uploadData.json", json.dumps(resp))

        return resp


    def ingestToEnvizi (self, main_data, uploadedFile):
        resp = self.processForIngestion(main_data, uploadedFile, True)
        return resp

    def viewInScreen (self, main_data, uploadedFile):
        resp = self.processForIngestion(main_data, uploadedFile, False)
        return resp
    
    def processForIngestion (self, main_data, uploadedFile, pushToS3):
        self.logger.info("processForIngestion ... : ")

        ### Retrive locations and accounts
        locations = []
        accounts = []
        account_styles = []
        if (self.LOAD_ENVIZI_DATA == "TRUE") : 
            list  = self.enviziMain.exportLocation()
            locations = list["data"]
            list = self.enviziMain.exportAccounts()
            accounts = list["data"]        

        ### Read excel content
        original_df = pd.read_excel(uploadedFile)

        ### template_columns
        envizi_template = main_data["envizi_template"]
        template_columns = self.templateMain.getTemplateColumns(envizi_template)

        fields = main_data["fields"]

        ### Process rows
        processed_data = []
        validation_errors = {}
        for i, row in original_df.iterrows():
            processed_row = {}
            index = 0
            for template_column in template_columns:
                # template_column_text = template_column["text"]
                template_column_text = template_column

                ### Formulate the value for the column
                uploaded_column_data = self.excelProDataGiver.obtainValueForColumn (fields, row, template_column_text)
                processed_row[template_column_text] = uploaded_column_data

                ### Validation
                errorText = self.templateDataValidator.validateData(template_column_text , uploaded_column_data, locations, account_styles)
                if errorText :
                    DictionaryUtil.appendIfDuplicate(validation_errors, errorText, i+1)

                index = index + 1

            ### Append the processed row to the list
            processed_data.append(processed_row)

        ### Generate the excel and push to S3
        resp = self.templateMain.generate_excel_and_push_to_s3(envizi_template, processed_data, pushToS3)

        ### Generate Response
        resp["validation_errors"] = validation_errors
        resp["template_columns"] = template_columns

        self.fileUtil.writeInFileWithCounter("processForIngestion.json", json.dumps(resp))

        return resp