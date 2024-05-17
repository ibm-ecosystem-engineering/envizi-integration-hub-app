import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

from typing import Dict, Optional, Any, Iterable, List
import uuid

# import getpass
import logging 
import os, json

from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.DictionaryUtil import DictionaryUtil
from util.ApiUtil import ApiUtil
from util.DateUtils import DateUtils
from util.ExcelUtil import ExcelUtil
from excel.ExcelProcessor import ExcelProcessor
from webhook.WebhookDB import WebhookDB
from webhook.WebhookEnviziMapping import WebhookEnviziMapping
from webhook.WebhookS3 import WebhookS3
from webhook.WebhookRun import WebhookRun
from CommonConstants import *
from webhook.WebhookDataGiver import WebhookDataGiver
from webhook.WebhookDataValidator import WebhookDataValidator

from envizi.EnviziMain import EnviziMain

class WebhookMain(object):

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
        self.DATA_STORE_FOLDER = os.getenv("DATA_STORE_FOLDER") 
        self.WEBHOOK_FOLDER = self.DATA_STORE_FOLDER + "/webhook/"
        self.WEBHOOK_FILE = self.WEBHOOK_FOLDER + "/webhook.json"
        self.excelUtil = ExcelUtil()
        self.excelProcessor = ExcelProcessor(self.fileUtil, self.configUtil)
        self.webhookDB = WebhookDB(self.fileUtil, self.configUtil)
        self.webhookEnviziMapping = WebhookEnviziMapping(self.fileUtil, self.configUtil)
        self.webhookS3 = WebhookS3(self.fileUtil, self.configUtil)
        self.webhookRun = WebhookRun(self.fileUtil, self.configUtil)
        self.enviziMain = EnviziMain(self.fileUtil, self.configUtil)
        self.webhookDataGiver = WebhookDataGiver(self.fileUtil, self.configUtil)
        self.webhookDataValidator = WebhookDataValidator(self.fileUtil, self.configUtil)

    def loadWebhooks(self):
        self.logger.info("loadWebhooks  ... ")

        data = self.fileUtil.loadJsonFileContent(self.WEBHOOK_FILE)

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("webhook.json", json.dumps(data))

        resp = {
            "msg": "Webhooks loaded successfully",
            "data": data,
        }

        return resp
    
    def loadWebhook(self, payload):
        self.logger.info("loadWebhook  ... ")
        self.logger.info("loadWebhook : " + json.dumps(payload))

        ### Retrieve webhook details from DB (file)
        id = payload["id"]
        webhook_detail_data = self.webhookDB.loadWebhookDetailById(id)

        ### Run webhook
        webhook_execute_response = self.webhookRun.run_webhook(webhook_detail_data)

        resp = {
            "msg": "Webhook data is loaded successfully",
            "data": webhook_detail_data,
            "webhook_response": webhook_execute_response
        }

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("webhook.json", json.dumps(resp))

        return resp


    def loadWebhookNew(self, payload):
        self.logger.info("loadWebhookNew  ... ")
        self.logger.info("loadWebhookNew : " + json.dumps(payload))

       ### Retrive locations and accounts
        locations = []
        accounts = []
        if (self.LOAD_ENVIZI_DATA == "TRUE") : 
            list  = self.enviziMain.exportLocation()
            locations = list["data"]
            list = self.enviziMain.exportAccounts()
            accounts = list["data"]

        ### Generate Empty Data
        webhook_detail_data = self.webhookEmptyDataGiver.generateEmptyData(locations, accounts)

        resp = {
            "msg": "Webhook data is loaded successfully",
            "data": webhook_detail_data,
        }

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("webhook.json", json.dumps(resp))

        return resp


    def loadWebhookTemplateChange(self, payload):
        self.logger.info("loadWebhookTemplateChange  ... ")
        self.logger.info("loadWebhookTemplateChange : " + json.dumps(payload))

        ### Retrive locations and accounts
        locations = []
        accounts = []
        if (self.LOAD_ENVIZI_DATA == "TRUE") : 
            list  = self.enviziMain.exportLocation()
            locations = list["data"]
            list = self.enviziMain.exportAccounts()
            accounts = list["data"]

        ### Generate fields based on template
        self.webhookEmptyDataGiver.populateFields(payload, locations, accounts)

        resp = {
            "msg": "Webhook data is loaded successfully",
            "data": payload,
        }

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("excelpro.json", json.dumps(resp))

        return resp
   

    def load_webhook_response(self, payload):
        self.logger.info("load_webhook_response  ... ")
        self.logger.info("load_webhook_response : " + json.dumps(payload))

        ### Run webhook
        webhook_execute_response = self.webhookRun.run_webhook(payload)

        resp = {
            "msg": "Webhook data is refreshed successfully",
            "data": webhook_execute_response
        }

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("webhook_execute_response.json", json.dumps(resp))

        return resp
    
    def saveWebhook(self, payload):
        self.logger.info("saveWebhook  ... ")

        ### Save webhook master
        id = self.webhookDB.saveWebhookMaster(payload)
        payload["id"] = id

        ### Save webhook detail
        result = self.webhookDB.saveWebhookDetail(payload)

        ### Run webhook
        webhook_response = self.webhookRun.run_webhook(payload)

        resp = {
            "msg": "Webhook is saved successfully",
            "data": result,
            "webhook_response" : webhook_response
        }
        return resp
    
    def updateWebhook(self, payload):
        self.logger.info("updateWebhook  ... ")

        ### Save webhook detail
        result = self.webhookDB.saveWebhookDetail(payload)
        resp = {
            "msg": "Webhook is updated successfully",
            "data": result
        }
        return resp

    def deleteWebhook(self, payload):
        self.logger.info("deleteWebhook  ... ")
        result = self.webhookDB.deleteWebhook(payload)
        resp = {
            "msg": "Webhook data is deleted successfully",
            "data": result
        }
        return resp

    def executeWebhook(self, payload):
        self.logger.info("executeWebhook  ... ")

        ### Retrieve webhook details from DB (file)
        id = payload["id"]
        webhook_detail_data = self.webhookDB.loadWebhookDetailById(id)

        ### Process
        resp = self.processForIngestion (webhook_detail_data, True)
        return resp

    ### User wants to see the UDC data while editiing the webhook
    def previewWebhook(self, payload):
        self.logger.info("previewWebhook  ... ")
        resp = self.processForIngestion (payload, False)
        return resp
    
    def processForIngestion (self, webhook_detail_data, pushToS3):
        self.logger.info("processForIngestion ... : ")

        envizi_template = webhook_detail_data["envizi_template"]

        ### Retrive locations and accounts
        locations = []
        accounts = []
        account_styles = []
        if (self.LOAD_ENVIZI_DATA == "TRUE") : 
            list  = self.enviziMain.exportLocation()
            locations = list["data"]
            list = self.enviziMain.exportAccounts()
            accounts = list["data"]        

        ### Run webhook
        webhook_execute_response = self.webhookRun.run_webhook(webhook_detail_data)

        ### template_columns
        template_columns = self.webhookEmptyDataGiver.getTemplateColumns(envizi_template)

        ### Mapping
        resp_mapping = self.webhookEnviziMapping.map_webhook_data_to_envizi_format(webhook_detail_data, webhook_execute_response, template_columns)
        processed_data = resp_mapping["processed_data"] 
        validation_errors = resp_mapping["validation_errors"] 

        # Specify the filename for the new Excel file
        filePrefix = self.excelProDataGiver.getExcelFilePrefix(envizi_template)
        output_filename = filePrefix + DateUtils.getSimpleCurrentDateTimeString() + ".xlsx"
        fileNameWithPath = self.fileUtil.getFileNameWithoutCounter(output_filename)
        self.logger.info("processForIngestion uploaded fileName ... : " + output_filename)

        self.fileUtil.writeInFileWithCounter("my-data.json", json.dumps(processed_data))

        # Write the processed DataFrame to a new Excel file
        sheetName = self.excelProDataGiver.getExcelFileSheetName(envizi_template)
        self.excelUtil.generateExcel(fileNameWithPath, sheetName, processed_data)

        # Write the processed DataFrame to a new Excel file
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