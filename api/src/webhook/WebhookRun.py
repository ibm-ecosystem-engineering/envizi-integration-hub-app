import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

import logging 
import os, json

from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.DictionaryUtil import DictionaryUtil
from util.ApiUtil import ApiUtil
from CommonConstants import *

 
class WebhookRun(object):

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


    def run_webhook(self, webhook_detail_data):
        self.logger.info(f"run_webhook  ... : {json.dumps(webhook_detail_data)}")

        url = DictionaryUtil.getValue_key1(webhook_detail_data, "url", "")

        ### Execute webhook
        webhook_execute_response = {}
        if (url and url != "") :
            webhook_execute_response = ApiUtil.callAPI("run_webhook", webhook_detail_data, {})
            ### Write updated data in ouput file
            self.fileUtil.writeInFileWithCounter("run_webhook-webhook_execute_response.json", json.dumps(webhook_execute_response))

        ### Write updated data in ouput file
        self.fileUtil.writeInFileWithCounter("run_webhook-webhook_execute_response.json", json.dumps(webhook_execute_response))

        return webhook_execute_response

