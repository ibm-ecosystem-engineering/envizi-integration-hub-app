import os
from util.ConfigUtil import ConfigUtil
import logging
from CommonConstants import *
from dotenv import load_dotenv

import json

from util.DateUtils import DateUtils
from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.DictionaryUtil import DictionaryUtil
from util.ExcelUtil import ExcelUtil
from util.MathUtil import MathUtil
from excel.ExcelProcessor import ExcelProcessor

class TemplateMain(object):

    def __init__(
        self,
        configUtil: ConfigUtil,
    ) -> None:
        self.configUtil = configUtil
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

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
        self.excelProcessor = ExcelProcessor(self.fileUtil, self.configUtil)
        self._init_config()

    def _init_config(self):
        self.DATA_STORE_FOLDER = os.getenv("DATA_STORE_FOLDER") 
        self.EXCELPRO_FOLDER = self.DATA_STORE_FOLDER + "/excelpro/"
        self.EXCELPRO_FILE = self.EXCELPRO_FOLDER + "/excelpro.json"
        self.excelUtil = ExcelUtil()

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


    def generate_excel_and_push_to_s3(self, envizi_template, processed_data, pushToS3) : 
            # Specify the filename for the new Excel file
        filePrefix = self.getExcelFilePrefix(envizi_template)
        output_filename = filePrefix + DateUtils.getSimpleCurrentDateTimeString() + ".xlsx"
        fileNameWithPath = self.fileUtil.getFileNameWithoutCounter(output_filename)
        self.logger.info("ingestToEnvizi uploaded fileName ... : " + output_filename)

        ### Write it in json..
        # self.fileUtil.writeInFileWithCounter("my-data.json", json.dumps(processed_data))

        # Write the processed DataFrame to a new Excel file
        sheetName = self.getExcelFileSheetName(envizi_template)
        self.excelUtil.generateExcel(fileNameWithPath, sheetName, processed_data)

        ### Push file to S3
        if (pushToS3) :
            msg = "The data is mapped to Envizi format successfully. \n The file " + fileNameWithPath + " is pushed to s3 successfully."
            s3FileName = self.excelProcessor.pushFileToS3(fileNameWithPath)
        else :
            s3FileName = ""
            msg = "The data is mapped to Envizi format successfully."

        ### Generate Response
        resp = {
                "uploadedFile" : fileNameWithPath,
                "s3FileName" : s3FileName,
                "processed_data" : processed_data,
                "msg": msg
                }
        return resp