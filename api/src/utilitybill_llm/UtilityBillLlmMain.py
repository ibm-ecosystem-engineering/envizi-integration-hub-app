import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv
import pandas as pd

import logging 
import os, json
from s3.S3Main import S3Main

from util.DateUtils import DateUtils
from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.ExcelUtil import ExcelUtil
from excel.ExcelProcessor import ExcelProcessor
from util.DictionaryUtil import DictionaryUtil
from utilitybill_llm.UtilityBillLlmProcessor import UtilityBillLlmProcessor
from template.TemplateMain import TemplateMain

import time

# my_script.py
from CommonConstants import *

class UtilityBillLlmMain(object):

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
        self.excelUtil = ExcelUtil()
        self.templateMain = TemplateMain(self.fileUtil, self.configUtil)

    def ingestToEnvizi (self):
        resp = self.exportUtilityBill(True)
        return resp

    def viewInScreen (self):
        resp = self.exportUtilityBill(False)
        return resp
    
    def exportUtilityBill(self, pushToS3):
        self.logger.info("UtilityBillLlmMain : exportUtilityBill  ... ")
        
        resp = {}
        try:
            ### call llm
            self.logger.info("UtilityBillLlmMain : exportUtilityBill 1 ... ")

            utilityBillLlmProcessor = UtilityBillLlmProcessor(self.fileUtil, self.configUtil)
            self.logger.info("UtilityBillLlmMain : exportUtilityBill 2 ... ")

            folder_path = self.configUtil.UTILITY_BILL_LLM_INPUT_FOLDER
            self.logger.info("UtilityBillLlmMain : exportUtilityBill 3 ... ")

            myList = utilityBillLlmProcessor.process_utility_bills(folder_path)
            self.logger.info("UtilityBillLlmMain : exportUtilityBill 4 ... ")

            ### Generate the excel and push to S3
            resp = self.templateMain.generate_excel_and_push_to_s3(TEMPLATE_NAME_POC, myList, pushToS3)
            self.logger.info("UtilityBillLlmMain : exportUtilityBill 5 ... ")

        except Exception as e:
            self.logger.info(f' UtilityBillLlmMain :  Error occured while processing utility bills using llm 3 : {e} \n\n')
            resp["msg"] = "Unable to load utility bills using llm"

        return resp

    def getColumns(self, ):
        myList = []
        myList.append("ORGANIZATION")
        myList.append("Location")
        myList.append("Account Style Caption")
        myList.append("Account Number")
        myList.append("Account Reference")
        myList.append("Account Supplier")
        myList.append("Record Start YYYY-MM-DD")
        myList.append("Record End YYYY-MM-DD")
        myList.append("Quantity")
        myList.append("Total cost (incl. Tax) in local currency")
        myList.append("Record Reference")
        myList.append("Record Invoice Number")
        myList.append("Record Data Quality")
        return myList

    def pushFileToS3(self, fileNameWithPathToSend):

        ### S3 filename
        s3FileName = FileUtil.extractFilename(fileNameWithPathToSend)
        self.logger.debug(f"S3 File Name :  {s3FileName} ")

        ### push excel file to S3
        s3Main = S3Main(self.configUtil)
        s3Main.pushFileToS3(fileNameWithPathToSend, s3FileName)

        return s3FileName