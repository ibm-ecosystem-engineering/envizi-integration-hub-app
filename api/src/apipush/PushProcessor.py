import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv
import pandas as pd

import requests
import logging 
import os, json
from CommonConstants import *


from util.MathUtil import MathUtil

from util.DateUtils import DateUtils
from util.DictionaryUtil import DictionaryUtil
from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.ExcelUtil import ExcelUtil
from s3.S3Main import S3Main

from datetime import datetime
from datetime import timedelta
from template.TemplateMain import TemplateMain

class PushProcessor(object):

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
        self.templateMain = TemplateMain(self.fileUtil, self.configUtil)

    def processForIngestion (self, envizi_template_name, payload, pushToS3):
        self.logger.info("processForIngestion ... : ")

        ### Mapping
        template_columns = self.templateMain.getTemplateColumns(envizi_template_name)
        self.logger.info(f"processForIngestion ... template_columns : {json.dumps(template_columns)} ")

        ### Process rows
        processed_data = []
        validation_errors = {}

        index = 0
        for row in payload :
            index = index + 1
            self.logger.info(f"processForIngestion ... : {index} ")
            self.logger.info(f"processForIngestion ... : {json.dumps(row)} ")

            processed_row = {}
            for template_column in template_columns:
                # template_column_text = template_column["text"]
                template_column_text = template_column

                ### Formulate the value for the column
                uploaded_column_data = self._findColumnValue(row, template_column_text)
                processed_row[template_column_text] = uploaded_column_data

            ### Append the processed row to the list
            processed_data.append(processed_row)

        ### Generate the excel and push to S3
        resp = self.templateMain.generate_excel_and_push_to_s3(envizi_template_name, processed_data, pushToS3)

        ### Generate Response
        return resp
    
    def _findColumnValue(self, json_data, column_name) : 
        resultValue = None
        ### If row_data is not empty..then try in row_data first
        if (json_data != None) :
            resultValue = DictionaryUtil.findValue(json_data, column_name)

        return resultValue