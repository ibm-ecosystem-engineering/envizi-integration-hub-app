import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

import logging 
import os, json

from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.DictionaryUtil import DictionaryUtil
from util.DateUtils import DateUtils
from util.NumberUtil import NumberUtil
from util.ApiUtil import ApiUtil
from CommonConstants import *
from scheduler.SchedulerDB import SchedulerDB
from webhook.WebhookEnviziMapping import WebhookEnviziMapping
from webhook.WebhookRun import WebhookRun
from template.TemplateMain import TemplateMain

 
class WebhookSchedulerJob(object):

    def __init__(
        self,
        configUtil: ConfigUtil
    ) -> None:
        self.configUtil = configUtil
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    def create_instances(self):
        self.logger.info("WebhookSchedulerJob : create_instances : ")
        fileUtil = FileUtil()
        fileUtil.start()

        self.webhookEnviziMapping = WebhookEnviziMapping(fileUtil, self.configUtil)
        self.webhookRun = WebhookRun(fileUtil, self.configUtil)
        self.templateMain = TemplateMain(fileUtil, self.configUtil)
        self.schedulerDB = SchedulerDB(fileUtil, self.configUtil)

    def __call__(self, webhook_detail_data):
        self.logger.info("WebhookSchedulerJob : process started ... : ")

        ### Create instances (init)
        self.create_instances()

        ### Job Id
        job_id = DictionaryUtil.getValue_key1(webhook_detail_data, "id", "")

        ### Create Job status Entry
        my_data = self.schedulerDB.create_job_started_entry(SCHEDULER_TYPE_WEBHOOK, job_id)

        ### Ingest into Envizi
        resp = self.processForIngestion(webhook_detail_data)

        ### Update Job status Entry
        my_data = self.schedulerDB.update_job_completed_entry(my_data)

        return my_data
    
    def processForIngestion(self, webhook_detail_data):

        ### Run webhook
        webhook_execute_response = self.webhookRun.run_webhook(webhook_detail_data)

        ### template_columns
        envizi_template = webhook_detail_data["envizi_template"]
        template_columns = self.templateMain.getTemplateColumns(envizi_template)

        mydata = {}
        mydata["locations"] = []
        mydata["accounts"] = []           
        mydata["account_styles"] = []   
        mydata["webhook_detail_data"] = webhook_detail_data   
        mydata["webhook_execute_response"] = webhook_execute_response   
        mydata["template_columns"] = template_columns   

        ### Mapping
        resp_mapping = self.webhookEnviziMapping.map_webhook_data_to_envizi_format(mydata)
        processed_data = resp_mapping["processed_data"] 
        validation_errors = resp_mapping["validation_errors"] 

        ### Generate the excel and push to S3
        resp = self.templateMain.generate_excel_and_push_to_s3(envizi_template, processed_data, False)

        ### Generate Response
        resp["validation_errors"] = validation_errors
        return resp
    