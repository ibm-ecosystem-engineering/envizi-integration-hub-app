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
from excelpro.ExcelProDataValidator import ExcelProDataValidator

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
        self.excelProDataValidator = ExcelProDataValidator(self.fileUtil, self.configUtil)
        self.enviziMain = EnviziMain(self.fileUtil, self.configUtil)
        

    def loadAll(self):
        self.logger.info("loadExcelPros  ... ")

        data = self.fileUtil.loadJsonFileContent(self.EXCELPRO_FILE)

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("excelpro.json", json.dumps(data))

        resp = {
            "msg": "ExcelPros loaded successfully",
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
            "msg": "ExcelPro data is loaded successfully",
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
            "msg": "ExcelPro data is loaded successfully",
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
            "msg": "ExcelPro data is loaded successfully",
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
            "msg": "ExcelPro is saved successfully",
            "data": result,
        }
        return resp
    
    def deleteExcelPro(self, payload):
        self.logger.info("deleteExcelPro  ... ")
        result = self.excelproDB.deleteExcelPro(payload)
        resp = {
            "msg": "ExcelPro data is deleted successfully",
            "data": result
        }
        return resp


    def uploadData (self, file, envizi_template):

        ## Save the file
        fileName = file.filename
        self.logger.info("uploadData uploaded fileName ... : " + fileName)
        fileNameWithPath = self.fileUtil.getFileNameWithoutCounter(fileName)
        file.save(fileNameWithPath)

        template_columns = self.excelProDataGiver.getTemplateColumns(envizi_template)

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


    def ingestToEnvizi (self, template_columns, envizi_template, uploadedFile, fields):
        resp = self.processForIngestion(template_columns, envizi_template, uploadedFile, fields, True)
        return resp


    def viewInScreen (self, template_columns, envizi_template, uploadedFile, fields):
        resp = self.processForIngestion(template_columns, envizi_template, uploadedFile, fields, False)
        return resp
    

    def processForIngestion (self, template_columns, envizi_template, uploadedFile, fields, pushToS3):
        self.logger.info("processForIngestion ... : ")

        ### Get Envizi Template Columns
        template_columns = self.excelProDataGiver.getTemplateColumns(envizi_template)

        ### Retrive locations and accounts
        locations = []
        accounts = []
        account_styles = []
        if (self.LOAD_ENVIZI_DATA == "TRUE") : 
            list  = self.enviziMain.exportLocation()
            locations = list["data"]
            list = self.enviziMain.exportAccounts()
            accounts = list["data"]        

        original_df = pd.read_excel(uploadedFile)
        processed_data = []
        validation_errors = []

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
                errorText = self.excelProDataValidator.validateData(i, template_column_text , uploaded_column_data, locations, accounts, account_styles)
                if errorText :
                    validation_errors.append(errorText)

                index = index + 1

            # Append the processed row to the list
            processed_data.append(processed_row)

        # Specify the filename for the new Excel file
        filePrefix = self.excelProDataGiver.getExcelFilePrefix(envizi_template)
        output_filename = filePrefix + DateUtils.getSimpleCurrentDateTimeString() + ".xlsx"
        fileNameWithPath = self.fileUtil.getFileNameWithoutCounter(output_filename)
        self.logger.info("ingestToEnvizi uploaded fileName ... : " + output_filename)

        ### Write it in json..
        self.fileUtil.writeInFileWithCounter("my-data.json", json.dumps(processed_data))

        # Write the processed DataFrame to a new Excel file
        sheetName = self.excelProDataGiver.getExcelFileSheetName(envizi_template)
        self.excelUtil.generateExcel(fileNameWithPath, sheetName, processed_data)

        ### Push file to S3
        if (pushToS3) :
            msg = "The file " + fileNameWithPath + " is pushed to s3 successfully."
            s3FileName = self.excelProcessor.pushFileToS3(fileNameWithPath)
        else :
            s3FileName = ""
            msg = "The processing completed successfully."

        ### Generate Response
        resp = {
                "uploadedFile" : fileNameWithPath,
                "s3FileName" : s3FileName,
                "processed_data" : processed_data,
                "validation_errors" : validation_errors,
                "msg": msg
                }
        return resp

