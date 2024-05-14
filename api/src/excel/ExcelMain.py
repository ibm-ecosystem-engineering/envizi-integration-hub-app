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
from util.DictionaryUtil import DictionaryUtil
from excel.ExcelProcessor import ExcelProcessor
import time


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

        ### Push to S3
        s3FileName = self.excelProcessor.pushFileToS3(fileName)

        # Convert excel to JSON
        processed_data = self.excelUtil.getExcelAsJsonArray(fileName)
        processed_data_columns = self.excelUtil.readColumnName(fileName)

        resp = {
                "file_name": s3FileName,
                "processed_data" : processed_data,
                "processed_data_columns" : processed_data_columns,
                "msg": "The file " + s3FileName + " is ingested successfully"
                }

        return resp
    
    def loadTemplatePOC (self, file):
        resp = self.loadTemplate2(file, TEMPLATE_POC_ACCOUNT_SETUP_AND_DATA_LOAD)
        return resp

    def loadTemplateASDL (self, file):
        resp = self.loadTemplate2(file, TEMPLATE_ACCOUNT_SETUP_AND_DATA_LOAD_PMC)
        return resp

    def ingestTemplatePOC (self, template_columns, uploaded_columns, uploadedFile, data_mapping):
        resp = self.ingestExcel(template_columns, uploaded_columns, uploadedFile, data_mapping, FILE_PREFIX_POC_ACCOUNT_SETUP_AND_DATA_LOAD, SHEET_NAME_POC_ACCOUNT_SETUP_AND_DATA_LOAD)
        return resp

    def ingestTemplateASDL (self, template_columns, uploaded_columns, uploadedFile, data_mapping):
        resp = self.ingestExcel(template_columns, uploaded_columns, uploadedFile, data_mapping, FILE_PREFIX_ACCOUNT_SETUP_AND_DATA_LOAD_PMC, SHEET_NAME_ACCOUNT_SETUP_AND_DATA_LOAD_PMC)
        return resp


    def obtainValueForColumn (self, data_mapping, excelRow, template_column_text):
        result = ""

        for field_data in data_mapping["pageData"]:
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
                                result = result + str(curr_value)
                            else :
                                result = result + str(curr_value)

                        operation_value_prev = operation_value

        return result


    def ingestExcel (self, template_columns, uploaded_columns, uploadedFile, data_mapping, filePrefix, sheetName):
        original_df = pd.read_excel(uploadedFile)
        processed_data = []

        for i, row in original_df.iterrows():
            processed_row = {}
            index=0
            for template_column in template_columns:
                # template_column_text = template_column["text"]
                template_column_text = template_column

                # uploaded_column_text = uploaded_columns[index]["text"]
                # uploaded_column_data = row.loc[uploaded_column_text]
                uploaded_column_data = self.obtainValueForColumn (data_mapping, row, template_column_text)

                self.logger.info("ingestTemplatePOC template_column_text ... : " + template_column_text)
                self.logger.info("ingestTemplatePOC uploaded_column_data ... : " + str(uploaded_column_data))

                # if (template_column_text == "Record Start YYYY-MM-DD" or template_column_text == "Record End YYYY-MM-DD") :
                #     processed_row[template_column_text] = DateUtils.timeStampToDateString(pd.to_datetime(uploaded_column_data, unit='s'))
                # else :
                #     processed_row[template_column_text] = uploaded_column_data
                processed_row[template_column_text] = uploaded_column_data

                index = index + 1

            # Append the processed row to the list
            processed_data.append(processed_row)

        # Specify the filename for the new Excel file
        output_filename = filePrefix + DateUtils.getSimpleCurrentDateTimeString() + ".xlsx"
        fileNameWithPath = self.fileUtil.getFileNameWithoutCounter(output_filename)
        self.logger.info("ingestTemplatePOC uploaded fileName ... : " + output_filename)

        ### Write it in json..
        self.fileUtil.writeInFileWithCounter("my-data.json", json.dumps(processed_data))

        # Write the processed DataFrame to a new Excel file
        self.excelUtil.generateExcel(fileNameWithPath, sheetName, processed_data)

        ### Push file to S3
        s3FileName = self.excelProcessor.pushFileToS3(fileNameWithPath)

        ### Generate Response
        resp = {
                "uploadedFile" : fileNameWithPath,
                "s3FileName" : s3FileName,
                "processed_data" : processed_data,
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
        template_columns = self.excelUtil.readColumnName(template_file_name)

        ### Source
        list = self.excelUtil.readColumnName(fileNameWithPath)
        uploaded_columns = []
        for item in list:
            self.logger.info("loadTemplate template_file_name item :" + item + ":")
            if (item != "") :
                uploaded_columns.append(item)

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


    def loadTemplate2 (self, file, templateName):
        ## Save the file
        fileName = file.filename
        self.logger.info("loadTemplate2 uploaded fileName ... : " + fileName)
        fileNameWithPath = self.fileUtil.getFileNameWithoutCounter(fileName)
        file.save(fileNameWithPath)

        # time.sleep(5)

        ### Destination file
        template_file_name = os.getenv("DATA_FOLDER", "") + "/templates/" + templateName
        self.logger.info("loadTemplate2 template_file_name ... : " + template_file_name)
        template_columns = self.excelUtil.readColumnName(template_file_name)

        ### Source
        list = self.excelUtil.readColumnName(fileNameWithPath)
        uploaded_columns = []
        for item in list:
            self.logger.info("loadTemplate2 template_file_name item :" + item + ":")
            if (item != "") :
                uploaded_columns.append(item)

        # uploaded_array = uploaded_columns
        # template_array = template_columns
        # max_length = max(len(uploaded_columns), len(template_columns))
        # for i in range(max_length):
        #     col1 = template_columns[i] if i < len(template_columns) else ''
        #     col2 = uploaded_columns[i] if i < len(uploaded_columns) else ''
            
        #     item1 = {"id": i,  "text": col1}
        #     template_array.append(item1)

        #     item2 = {"id": i,  "text": col2, "difference" : False}
        #     uploaded_array.append(item2)

        #     if col1 != col2:
        #         item2["difference"] = True

        resp = {
                "uploaded_columns": uploaded_columns,
                "template_columns": template_columns,
                "uploadedFile": fileNameWithPath,
                "msg": "The columns of the " + fileName + " file have been successfully loaded"
                }

        return resp
