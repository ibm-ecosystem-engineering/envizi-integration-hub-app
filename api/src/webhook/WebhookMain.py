import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

from typing import Dict, Optional, Any, Iterable, List
import uuid
import time
import logging 
import os, json

from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.DictionaryUtil import DictionaryUtil
from util.StringUtil import StringUtil
from util.ApiUtil import ApiUtil
from util.DateUtils import DateUtils
from util.NumberUtil import NumberUtil
from util.ExcelUtil import ExcelUtil
from util.JsonUtil import JsonUtil
from excel.ExcelProcessor import ExcelProcessor
from webhook.WebhookDB import WebhookDB
from webhook.WebhookEnviziMapping import WebhookEnviziMapping
from webhook.WebhookRun import WebhookRun
from webhook.WebhookScheduler import WebhookScheduler
from CommonConstants import *
from webhook.WebhookDataGiver import WebhookDataGiver
from template.TemplateMain import TemplateMain
from scheduler.SchedulerMain import SchedulerMain
from template.TemplateDataValidator import TemplateDataValidator
from envizi.EnviziMain import EnviziMain
from scheduler.SchedulerDB import SchedulerDB

class WebhookMain(object):

    def __init__(
        self,
        fileUtil: FileUtil,
        configUtil: ConfigUtil,
        schedulerMain: SchedulerMain
    ) -> None:
        self.fileUtil = fileUtil
        self.configUtil = configUtil
        self.schedulerMain = schedulerMain
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())
        self._init_config()

    def _init_config(self):
        self.LOAD_ENVIZI_DATA = os.getenv("LOAD_ENVIZI_DATA") 
        
        self.enable_real_time = False
        if (os.getenv("ENABLE_REAL_TIME", "FALSE") == "TRUE") :
            self.enable_real_time = True

        self.excelUtil = ExcelUtil()
        self.excelProcessor = ExcelProcessor(self.fileUtil, self.configUtil)
        self.webhookDB = WebhookDB(self.fileUtil, self.configUtil)
        self.webhookEnviziMapping = WebhookEnviziMapping(self.fileUtil, self.configUtil)
        self.webhookRun = WebhookRun(self.fileUtil, self.configUtil)
        self.webhookScheduler = WebhookScheduler(self.configUtil, self.schedulerMain)
        self.enviziMain = EnviziMain(self.fileUtil, self.configUtil)
        self.webhookDataGiver = WebhookDataGiver(self.fileUtil, self.configUtil)
        self.templateMain = TemplateMain(self.fileUtil, self.configUtil)
        self.templateDataValidator = TemplateDataValidator(self.fileUtil, self.configUtil)


    def loadWebhooks(self):
        self.logger.info("loadWebhooks  ... ")

        ### Fetch
        webhooks = self.__loadWebhooks()

        resp = {
            "msg": "Webhooks loaded successfully",
            "data": webhooks,
            "enable_real_time" : self.enable_real_time
        }
        return resp
    
    def loadWebhook(self, payload):
        self.logger.info("loadWebhook  ... ")

        job_id = payload["id"]

        ### Retrieve webhook details from DB (file)
        webhook_detail_data = self.webhookDB.loadWebhookDetailById(job_id)

        ### Run webhook
        webhook_execute_response = self.webhookRun.run_webhook(webhook_detail_data)
        
        ### Retrieve jobFileContent
        jobFileContent = self.webhookScheduler.loadJobFileContent(job_id)
        jobFileContentColumns = self.webhookScheduler.loadJobFileContentColumns()

        resp = {
            "msg": "Webhook data is loaded successfully",
            "data": webhook_detail_data,
            "webhook_response": webhook_execute_response,
            "job_file_content": jobFileContent,
            "job_file_content_columns": jobFileContentColumns
        }

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("webhook.json", json.dumps(resp))

        return resp



    def __loadWebhooks(self):
        self.logger.info("__loadWebhooks  ... ")

        ### Fetch
        webhooks = self.webhookDB.loadWebhookMasterFileContent()

        ### create jobs for each webhooks
        try:
            for webhook in webhooks:
                id = DictionaryUtil.getValue_key1(webhook, "id", "")

                ### Retrieve webhook details from DB (file)
                webhook_detail_data = self.webhookDB.loadWebhookDetailById(id)

                isSchedulerOn = DictionaryUtil.getValue_key1(webhook_detail_data, "isSchedulerOn", False)
                webhook["isSchedulerOn"] = StringUtil.boolean_to_text(isSchedulerOn)

                isRunning = self.schedulerMain.is_job_running(id)
                webhook["isRunning"] = StringUtil.boolean_to_text(isRunning)

        except Exception as e:
            self.logger.info(f' Unable to Load webhooks : {e} \n\n')

        self.fileUtil.writeInFileWithCounter("webhook.json", json.dumps(webhooks))

        return webhooks
    

    def loadWebhookNew(self, payload):
        self.logger.info("loadWebhookNew  ... ")
        self.logger.debug("loadWebhookNew : " + json.dumps(payload))

       ### Retrive locations and accounts
        locations = []
        accounts = []
        if (self.LOAD_ENVIZI_DATA == "TRUE") : 
            list  = self.enviziMain.exportLocation()
            locations = list["data"]
            list = self.enviziMain.exportAccounts()
            accounts = list["data"]

        ### Generate Empty Data
        webhook_detail_data = self.webhookDataGiver.generateEmptyData(locations, accounts)

        resp = {
            "msg": "Webhook data is loaded successfully",
            "data": webhook_detail_data,
        }

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("webhook.json", json.dumps(resp))

        return resp


    def loadWebhookTemplateChange(self, payload):
        self.logger.info("loadWebhookTemplateChange  ... ")
        self.logger.debug("loadWebhookTemplateChange : " + json.dumps(payload))

        ### Retrive locations and accounts
        locations = []
        accounts = []
        if (self.LOAD_ENVIZI_DATA == "TRUE") : 
            list  = self.enviziMain.exportLocation()
            locations = list["data"]
            list = self.enviziMain.exportAccounts()
            accounts = list["data"]

        ### Generate fields based on template
        self.webhookDataGiver.populateFields(payload, locations, accounts)

        resp = {
            "msg": "Webhook data is loaded successfully",
            "data": payload,
        }

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("excelpro.json", json.dumps(resp))

        return resp
   

    def load_webhook_response(self, payload):
        self.logger.debug("load_webhook_response  ... ")
        # self.logger.debug("load_webhook_response : " + json.dumps(payload))

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
        self.logger.debug("saveWebhook  ... ")

        ### Save webhook master
        id = self.webhookDB.saveWebhookMaster(payload)
        payload["id"] = id

        ### Save webhook detail
        result = self.webhookDB.saveWebhookDetail(payload)

        ### Run webhook
        webhook_response = self.webhookRun.run_webhook(payload)

        ### addOrUpdateJobInScheduler Scheduler
        self.webhookScheduler.addOrUpdateJobInScheduler(payload)

        resp = {
            "msg": "Webhook is saved successfully",
            "data": result,
            "webhook_response" : webhook_response
        }
        return resp
    
    # def updateWebhook(self, payload):
    #     self.logger.info("updateWebhook  ... ")

    #     ### Save webhook detail
    #     result = self.webhookDB.saveWebhookDetail(payload)
    #     resp = {
    #         "msg": "Webhook is updated successfully",
    #         "data": result
    #     }
    #     return resp

    def deleteWebhook(self, payload):
        self.logger.info("deleteWebhook  ... ")

        ### removeFromScheduler
        self.webhookScheduler.removeJobFromScheduler(payload)

        ### Delete webhook
        result = self.webhookDB.deleteWebhook(payload)

        resp = {
            "msg": "Webhook data is deleted successfully",
            "data": result,
            "enable_real_time" : self.enable_real_time
        }
        return resp
    


    def startWebhook(self, payload):
        self.logger.info("startWebhook  ... ")

        job_id = payload["id"]

        ### Retrieve webhook details from DB (file)
        webhook_detail_data = self.webhookDB.loadWebhookDetailById(job_id)

        ### Add To Scheduler
        self.webhookScheduler.addOrUpdateJobInScheduler(webhook_detail_data)

        ### Fetch
        webhooks = self.__loadWebhooks()

        resp = {
            "msg": "Webhook is started successfully",
            "data": webhooks,
            "enable_real_time" : self.enable_real_time
        }
        return resp    

    def stopWebhook(self, payload):
        self.logger.info("stopWebhook  ... ")

        job_id = payload["id"]

        ### Retrieve webhook details from DB (file)
        webhook_detail_data = self.webhookDB.loadWebhookDetailById(job_id)

        ### removeFromScheduler
        self.webhookScheduler.removeJobFromScheduler(webhook_detail_data)

        ### Fetch
        webhooks = self.__loadWebhooks()

        resp = {
            "msg": "Webhook is stopped successfully",
            "data": webhooks,
            "enable_real_time" : self.enable_real_time
        }
        return resp    

    def ingestToEnvizi(self, payload):
        self.logger.info("ingestToEnvizi  ... ")
        ### Retrieve webhook details from DB (file)
        # id = payload["id"]
        # webhook_detail_data = self.webhookDB.loadWebhookDetailById(id)

        ### Process
        resp = self.processForIngestionFromUI(payload, True)

        return resp

    ### User wants to see the UDC data while editiing the webhook
    def viewInScreen(self, payload):
        self.logger.info("viewInScreen  ... ")
        resp = self.processForIngestionFromUI (payload, False)
        return resp
    

    def processForIngestionFromUI (self, webhook_detail_data, pushToS3):
        self.logger.info("WebhookEnviziIngest : processForIngestionFromUI ... : ")

        ### Retrive locations and accounts
        locations = []
        accounts = []
        if (self.LOAD_ENVIZI_DATA == "TRUE") : 
            list  = self.enviziMain.exportLocation()
            locations = list["data"]
            list = self.enviziMain.exportAccounts()
            accounts = list["data"]

        ### Run webhook
        webhook_execute_response = self.webhookRun.run_webhook(webhook_detail_data)

        ### template_columns
        envizi_template = webhook_detail_data["envizi_template"]
        template_columns = self.templateMain.getTemplateColumns(envizi_template)

        mydata = {}
        mydata["locations"] = locations
        mydata["accounts"] = accounts           
        mydata["account_styles"] = []   
        mydata["webhook_detail_data"] = webhook_detail_data   
        mydata["webhook_execute_response"] = webhook_execute_response   
        mydata["template_columns"] = template_columns   

        ### Mapping
        resp_mapping = self.webhookEnviziMapping.map_webhook_data_to_envizi_format(mydata)
        processed_data = resp_mapping["processed_data"] 
        validation_errors = resp_mapping["validation_errors"] 

        ### Generate the excel and push to S3
        resp = self.templateMain.generate_excel_and_push_to_s3(envizi_template, processed_data, pushToS3)

        ### Generate Response
        resp["validation_errors"] = validation_errors
        resp["template_columns"] = template_columns

        return resp