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
from discovery.DiscoveryHandler import DiscoveryHandler
from util.DictionaryUtil import DictionaryUtil
from s3.S3Main import S3Main
from template.TemplateMain import TemplateMain


import time


# my_script.py
from CommonConstants import *

class UtilityBillMain(object):

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
        self.logger.info("exportUtilityBill  ... ")

        resp = {}
        discoveryHandler = DiscoveryHandler(self.fileUtil, self.configUtil)
        try:
            my_result = discoveryHandler.load_utility_from_discovery()
            
            discovery_result = my_result["result"]

            myList = self.createRecordsData(discovery_result)

            ### Generate the excel and push to S3
            resp = self.templateMain.generate_excel_and_push_to_s3(TEMPLATE_NAME_POC, myList, pushToS3)

        except Exception as e:
            self.logger.info(f' Unable to load utility bills from discovery 1 : {e} \n\n')
            resp["msg"] = "Unable to load utility bills from discovery"

        return resp

    def createRecordsData(self, discovery_result):
        myList = []
            
        for row in discovery_result:

            supplier = str(DictionaryUtil.getValue_key1(row, "my_supplier", None))
            customer = str(DictionaryUtil.getValue_key1(row, "my_customer", None))
            print(" supplier --> " + supplier)
            print(" customer --> " + customer)

            myRow = {}
            myRow["ORGANIZATION"] = self.configUtil.ENVIZI_ORG_NAME
            myRow["Location"] = self.configUtil.UTILITY_BILL_OTHERS_LOCATION
            myRow["Account Style Caption"] = self.configUtil.UTILITY_BILL_OTHERS_ACCOUNT_STYLE
            myRow["Account Number"] = self.configUtil.ENVIZI_PREFIX + "-Utility-" + supplier + "-" + customer
            myRow["Account Reference"] = ""
            myRow["Account Supplier"] = supplier
            myRow["Record Start YYYY-MM-DD"] = DateUtils.convertDateFormatYYYYMMDD(DictionaryUtil.getValue_key1(row, "my_startdate", None))
            myRow["Record End YYYY-MM-DD"] = DateUtils.convertDateFormatYYYYMMDD(DictionaryUtil.getValue_key1(row, "my_enddate", None))
            myRow["Quantity"] = DictionaryUtil.getValue_key1(row, "my_qty", None)
            myRow["Total cost (incl. Tax) in local currency"] = DictionaryUtil.getValue_key1(row, "my_cost", None)
            myRow["Record Reference"] = DictionaryUtil.getValue_key1(row, "my_customer", None)
            myRow["Record Invoice Number"] = ""
            myRow["Record Data Quality"] = ""

            myList.append(myRow)

        return myList
    
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