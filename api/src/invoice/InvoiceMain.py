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


import time


# my_script.py
from CommonConstants import *

class InvoiceMain(object):

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

    def exportInovice(self):
        self.logger.info("exportInovice  ... ")

        resp = {}
        discoveryHandler = DiscoveryHandler(self.fileUtil, self.configUtil)
        try:
            my_result = discoveryHandler.load_invoice_from_discovery()
            discovery_result = my_result["result"]

            myList = self.createRecordsData(discovery_result)
            fileNameWithPath = self.fileUtil.getFileNameWithoutCounter("Account-Setup-and-Data-Load-AI-Assist_" + DateUtils.getSimpleCurrentDateTimeString() + ".xlsx")
            self.logger.info(f' File Name : {fileNameWithPath} \n\n')

            # Write the processed DataFrame to a new Excel file
            self.excelUtil.generateExcel(fileNameWithPath, "Records to load", myList)

            resp["file_name"] = fileNameWithPath
            resp["processed_data"] = myList
            resp["processed_data_columns"] = self.getColumns()
            resp["msg"] = "The file " + fileNameWithPath + " is created successfully"

        except Exception as e:
            self.logger.info(f' Unable to load invoices from discovery : {e} \n\n')
            resp["msg"] = "Unable to load invoices from discovery"

        return resp

    def createRecordsData(self, discovery_result):
        myList = []
            
        for row in discovery_result:
            myRow = {}
            myRow["ORGANIZATION"] = self.configUtil.ENVIZI_ORG_NAME
            myRow["Location"] = "EIH Invoice"
            myRow["Account Style Caption"] = ""
            myRow["Account Supplier"] = DictionaryUtil.getValue_key1(row, "inv-supplier", None)
            myRow["Record Start YYYY-MM-DD"] = DictionaryUtil.getValue_key1(row, "inv-date", None)
            myRow["Record End YYYY-MM-DD"] = DictionaryUtil.getValue_key1(row, "inv-date", None)
            myRow["Spend in USD"] = ""
            myRow["Spend in Local Currency"] = DictionaryUtil.getValue_key1(row, "inv-total-cost", None)
            myRow["Record Reference"] = ""
            myRow["NLP Reference 1"] = DictionaryUtil.getValue_key1(row, "inv-goods", None)
            myRow["NLP Reference 2"] = DictionaryUtil.getValue_key1(row, "text", None)
            myRow["NLP Reference 3"] = ""
            myRow["NLP Reference 4"] = ""
            myRow["NLP Reference 5"] = ""
            myRow["AI Output Status"] = ""

            myList.append(myRow)

        return myList
    

    def getColumns(self, ):
        myList = []
        myList.append("ORGANIZATION")
        myList.append("Location")
        myList.append("Account Style Caption")
        myList.append("Account Supplier")
        myList.append("Record Start YYYY-MM-DD")
        myList.append("Record End YYYY-MM-DD")
        myList.append("Spend in USD")
        myList.append("Spend in Local Currency")
        myList.append("Record Reference")
        myList.append("NLP Reference 1")
        myList.append("NLP Reference 2")
        myList.append("NLP Reference 3")
        myList.append("NLP Reference 4")
        myList.append("NLP Reference 5")
        myList.append("AI Output Status")
        return myList