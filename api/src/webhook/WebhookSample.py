import os
import logging
from dotenv import load_dotenv

import logging 
from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil


class WebhookSample(object):

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

    def sample1Webhook(self):
        fileName = self.WEBHOOK_FOLDER + "/webhook-sample1.json"
        data = self.fileUtil.loadJsonFileContent(fileName)
        return data
    
    def sample2Webhook(self):
        fileName = self.WEBHOOK_FOLDER + "/webhook-sample2.json"
        data = self.fileUtil.loadJsonFileContent(fileName)
        return data
    
    def sample3Webhook(self):
        fileName = self.WEBHOOK_FOLDER + "/webhook-sample3.json"
        data = self.fileUtil.loadJsonFileContent(fileName)
        return data
    
    def sample4Webhook(self):
        fileName = self.WEBHOOK_FOLDER + "/webhook-sample4.json"
        data = self.fileUtil.loadJsonFileContent(fileName)
        return data

    def sample5Webhook(self):
        fileName = self.WEBHOOK_FOLDER + "/webhook-sample5.json"
        data = self.fileUtil.loadJsonFileContent(fileName)
        return data
    
    def sampleWebhook(self, name):
        fileName = self.WEBHOOK_FOLDER + "/" + name + ".json"
        data = self.fileUtil.loadJsonFileContent(fileName)
        return data

    