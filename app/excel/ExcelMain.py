import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv
import pandas as pd

import logging 
import os, json

from util.DateUtils import DateUtils
from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.ExcelUtil import ExcelUtil
from excel.ExcelProcessor import ExcelProcessor
import time


# my_script.py
from CommonConstants import *

class ExcelMain(object):

    def __init__(
        self,
        fileUtil: FileUtil,
        configUtil: ConfigUtil,
    ) -> None:
        load_dotenv()
        self.fileUtil = fileUtil
        self.configUtil = configUtil
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())
        self.excelProcessor = ExcelProcessor(self.fileUtil, self.configUtil)
        self.excelUtil = ExcelUtil()

    def uploadConfigConnector(self, file):
        ## Save the file
        fileName = file.filename
        self.logger.info("uploadConfigConnector uploaded fileName ... : " + fileName)

        file.save(fileName)

        s3FileName = self.excelProcessor.pushFileToS3(fileName)

        resp = {
                "file_name": s3FileName,
                "msg": "The file " + s3FileName + " is ingested successfully"
                }

        return resp
    
    def loadTemplatePOC (self, file):
        resp = self.loadTemplate(file, TEMPLATE_POC_ACCOUNT_SETUP_AND_DATA_LOAD)
        return resp

    def loadTemplateASDL (self, file):
        resp = self.loadTemplate(file, TEMPLATE_ACCOUNT_SETUP_AND_DATA_LOAD_PMC)
        return resp

    def ingestTemplatePOC (self, template_columns, uploaded_columns, uploadedFile):
        resp = self.ingestExcel(template_columns, uploaded_columns, uploadedFile, FILE_PREFIX_POC_ACCOUNT_SETUP_AND_DATA_LOAD, SHEET_NAME_POC_ACCOUNT_SETUP_AND_DATA_LOAD)
        return resp

    def ingestTemplateASDL (self, template_columns, uploaded_columns, uploadedFile):
        resp = self.ingestExcel(template_columns, uploaded_columns, uploadedFile, FILE_PREFIX_ACCOUNT_SETUP_AND_DATA_LOAD_PMC, SHEET_NAME_ACCOUNT_SETUP_AND_DATA_LOAD_PMC)
        return resp
    
    def ingestExcel (self, template_columns, uploaded_columns, uploadedFile, filePrefix, sheetName):
        original_df = pd.read_excel(uploadedFile)
        processed_data = []

        for i, row in original_df.iterrows():
            processed_row = {}
            index=0
            for template_column in template_columns:
                template_column_text = template_column["text"]

                uploaded_column_text = uploaded_columns[index]["text"]
                uploaded_column_data = row.loc[uploaded_column_text]

                self.logger.info("ingestTemplatePOC template_column_text ... : " + template_column_text)


                if (template_column_text == "Record Start YYYY-MM-DD" or template_column_text == "Record End YYYY-MM-DD") :
                    processed_row[template_column_text] = DateUtils.timeStampToDateString(pd.to_datetime(uploaded_column_data, unit='s'))
                else :
                    processed_row[template_column_text] = uploaded_column_data
                index = index + 1

            # Append the processed row to the list
            processed_data.append(processed_row)

        # Specify the filename for the new Excel file
        output_filename = filePrefix + DateUtils.getSimpleCurrentDateTimeString() + ".xlsx"
        fileNameWithPath = self.fileUtil.getFileNameWithoutCounter(output_filename)
        self.logger.info("ingestTemplatePOC uploaded fileName ... : " + output_filename)

        # Write the processed DataFrame to a new Excel file
        self.excelUtil.generateExcel(fileNameWithPath, sheetName, processed_data)

        ### Push file to S3
        s3FileName = self.excelProcessor.pushFileToS3(fileNameWithPath)

        ### Generate Response
        resp = {
                "uploadedFile" : fileNameWithPath,
                "s3FileName" : s3FileName,
                "msg": "The file " + fileNameWithPath + " is pushed to s3 successfully."
                }
        return resp


    def ingestExcel111 (self, template_columns, uploaded_columns, uploadedFile, filePrefix, sheetName):
        original_df = pd.read_excel(uploadedFile)
        processed_data = []

        for i, row in original_df.iterrows():
            processed_row = {}
            index=0
            for uploaded_column in uploaded_columns:
                uploaded_column_text = uploaded_column["text"]
                uploaded_column_data = row.loc[uploaded_column_text]

                template_column = template_columns[index]["text"]

                if (template_column == "Record Start YYYY-MM-DD" or template_column == "Record End YYYY-MM-DD") :
                    processed_row[template_column] = DateUtils.timeStampToDateString(pd.to_datetime(uploaded_column_data, unit='s'))
                else :
                    processed_row[template_column] = uploaded_column_data
                index = index + 1

            # Append the processed row to the list
            processed_data.append(processed_row)

        # Specify the filename for the new Excel file
        output_filename = filePrefix + DateUtils.getSimpleCurrentDateTimeString() + ".xlsx"
        fileNameWithPath = self.fileUtil.getFileNameWithoutCounter(output_filename);
        self.logger.info("ingestTemplatePOC uploaded fileName ... : " + output_filename)

        # Write the processed DataFrame to a new Excel file
        self.excelUtil.generateExcel(fileNameWithPath, sheetName, processed_data)

        ### Push file to S3
        s3FileName = self.excelProcessor.pushFileToS3(fileNameWithPath)

        ### Generate Response
        resp = {
                "uploadedFile" : fileNameWithPath,
                "s3FileName" : s3FileName,
                "msg": "The file " + fileNameWithPath + " is pushed to s3 successfully."
                }
        return resp

    def loadTemplate (self, file, templateName):
        ## Save the file
        fileName = file.filename
        self.logger.info("loadTemplate uploaded fileName ... : " + fileName)
        fileNameWithPath = self.fileUtil.getFileNameWithoutCounter(fileName)
        file.save(fileNameWithPath)

        # time.sleep(5)

        ### Destination file
        template_file_name = os.getenv("DATA_FOLDER", "") + "/templates/" + templateName
        self.logger.info("loadTemplate template_file_name ... : " + template_file_name)
        template_columns = self.excelProcessor.readColumnName(template_file_name)

        ### Source
        uploaded_columns = self.excelProcessor.readColumnName(fileNameWithPath)

        uploaded_array = []
        template_array = []
        max_length = max(len(uploaded_columns), len(template_columns))
        for i in range(max_length):
            col1 = template_columns[i] if i < len(template_columns) else ''
            col2 = uploaded_columns[i] if i < len(uploaded_columns) else ''
            
            item1 = {"id": i,  "text": col1}
            template_array.append(item1)

            item2 = {"id": i,  "text": col2, "difference" : False}
            uploaded_array.append(item2)

            if col1 != col2:
                item2["difference"] = True

        resp = {
                "uploaded_columns": uploaded_columns,
                "template_columns": template_columns,
                "uploaded_array": uploaded_array,
                "template_array": template_array,
                "uploadedFile": fileNameWithPath,
                "msg": "The columns of the " + fileName + " file have been successfully loaded"
                }

        return resp
