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
from util.ExcelUtil import ExcelUtil
from excel.ExcelProcessor import ExcelProcessor
from webhook.WebhookDB import WebhookDB
from webhook.WebhookEnviziMapping import WebhookEnviziMapping
from webhook.WebhookS3 import WebhookS3
from webhook.WebhookRun import WebhookRun
from CommonConstants import *

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
        self.fileUtil.writeInFileWithCounter("executeWebhook-1-payload.json", json.dumps(payload))

        ### Retrieve webhook details from DB (file)
        id = payload["id"]
        webhook_detail_data = self.webhookDB.loadWebhookDetailById(id)

        ### Run webhook
        webhook_execute_response = self.webhookRun.run_webhook(webhook_detail_data)

        ### Mapping
        processed_data = self.webhookEnviziMapping.map_webhook_data_to_envizi_format(webhook_detail_data, webhook_execute_response)

        ### Push Data to S3
        resp = self.webhookS3.createPOC_and_Push_to_s3(FILE_PREFIX_POC_ACCOUNT_SETUP_AND_DATA_LOAD, SHEET_NAME_POC_ACCOUNT_SETUP_AND_DATA_LOAD, processed_data)
        
        ### template_columns
        resp["template_columns"] = self.webhookEnviziMapping.getTemplateColumns()

        return resp
    

    def convertWebhook(self, payload):
        self.logger.info("convertWebhook  ... ")
        self.fileUtil.writeInFileWithCounter("convertWebhook-1-payload.json", json.dumps(payload))

        ### Retrieve existing content
        id = payload["id"]
        ### Don't load from the DB, just use what is there in the UI
        webhook_detail_data = payload

        ### Run webhook
        webhook_execute_response = self.webhookRun.run_webhook(webhook_detail_data)

        ### Mapping
        data = self.webhookEnviziMapping.map_webhook_data_to_envizi_format(webhook_detail_data, webhook_execute_response)

        ### template_columns
        template_columns = self.webhookEnviziMapping.getTemplateColumns()

        ### Generate Response
        resp = {
                "data" : data,
                "template_columns" : template_columns,
                "msg": "The processing completed successfully."
                }

        return resp