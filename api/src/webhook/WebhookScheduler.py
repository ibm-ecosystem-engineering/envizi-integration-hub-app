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
from scheduler.SchedulerMain import SchedulerMain
from webhook.WebhookSchedulerJob import WebhookSchedulerJob
from webhook.WebhookDB import WebhookDB

class WebhookScheduler(object):

    def __init__(
        self,
        configUtil: ConfigUtil,
        schedulerMain: SchedulerMain
    ) -> None:
        self.configUtil = configUtil
        self.schedulerMain = schedulerMain
        self.fileUtil = FileUtil()
        self.fileUtil.start()
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())
        self._init_config()

    def _init_config(self):
        self.enable_real_time = False
        if (os.getenv("ENABLE_REAL_TIME", "FALSE") == "TRUE") :
            self.enable_real_time = True
        self.DATA_STORE_FOLDER = os.getenv("DATA_STORE_FOLDER") 
        self.WEBHOOK_FOLDER = self.DATA_STORE_FOLDER + "/webhook/"
        self.WEBHOOK_FILE = self.WEBHOOK_FOLDER + "/webhook.json"
        self.schedulerDB = SchedulerDB(self.fileUtil, self.configUtil)
        self.webhookDB = WebhookDB(self.fileUtil, self.configUtil)

    def loadJobFileContent(self, job_id):
        resp = self.schedulerDB.loadJobFileContent(SCHEDULER_TYPE_WEBHOOK, job_id)
        return resp

    def loadJobFileContentColumns(self):
        resp = self.schedulerDB.loadJobFileContentColumns(SCHEDULER_TYPE_WEBHOOK)
        return resp

    def createJobsForWebhooks(self):
        self.logger.info("WebhookScheduler : createJobsForWebhooks stated ... ")

        if (self.enable_real_time) :
            ### Fetch all webhooks
            webhooks = self.webhookDB.loadWebhookMasterFileContent()

            ### create jobs for each webhooks
            try:
                for webhook in webhooks:
                    id = DictionaryUtil.getValue_key1(webhook, "id", "")

                    ### Retrieve webhook details from DB (file)
                    webhook_detail_data = self.webhookDB.loadWebhookDetailById(id)

                    self.addOrUpdateJobInScheduler(webhook_detail_data)
            except Exception as e:
                self.logger.info(f' Unable to process discovery result : {e} \n\n')
            else:
                self.logger.info(f"WebhookScheduler : enable_real_time  : {self.enable_real_time} ")
        self.logger.info("WebhookScheduler : createJobsForWebhooks  completed ... ")


    def addOrUpdateJobInScheduler(self, payload):
        self.logger.info("WebhookScheduler : addOrUpdateJobInScheduler  ... ")

        if (self.enable_real_time) :
            id = DictionaryUtil.getValue_key1(payload, "id", "")
            isSchedulerOn = DictionaryUtil.getValue_key1(payload, "isSchedulerOn", False)
            if (isSchedulerOn) :
                startDate = DictionaryUtil.getValue_key1(payload, "startDate", "")
                endDate = DictionaryUtil.getValue_key1(payload, "endDate", "")
                interval = DictionaryUtil.getValue_key1(payload, "interval", 60)

                if (startDate != "" and endDate != "" and id != "") :
                    startDate1 = DateUtils.stringToDate (startDate)
                    endDate1 = DateUtils.stringToDate (endDate)
                    interval1 = NumberUtil.stingToInt(interval, 60)

                    webhookSchedulerJob = WebhookSchedulerJob(self.configUtil)
                    self.schedulerMain.add_interval_job(webhookSchedulerJob, [payload], startDate1, endDate1, interval1, id)
            else :
                self.schedulerMain.remove_job(id)
        else:
            self.logger.info(f"WebhookScheduler : enable_real_time  : {self.enable_real_time} ")

    def removeJobFromScheduler(self, payload):
        self.logger.info("WebhookScheduler : removeJobFromScheduler  ... ")
        id = DictionaryUtil.getValue_key1(payload, "id", "")
        self.schedulerMain.remove_job(id)

        