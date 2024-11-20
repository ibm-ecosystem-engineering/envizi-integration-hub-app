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
from util.DictionaryUtil import DictionaryUtil
from apipush.PushProcessor import PushProcessor
import time


from CommonConstants import *

class PushMain(object):

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
        self.pushProcessor = PushProcessor(self.fileUtil, self.configUtil)

    def pushSetupConfig(self, payload):
        self.logger.info("pushSetupConfig started ... : ")
        self.fileUtil.writeInFileWithCounter("pushSetupConfig-input.json", json.dumps(payload))

        ### Push to S3
        resp = self.pushProcessor.processForIngestion(TEMPLATE_NAME_SETUP_CONFIG, payload, True)
        return resp

    def pushPOC(self, payload):
        self.logger.info("pushPOC started ... : ")
        self.fileUtil.writeInFileWithCounter("pushPOC-input.json", json.dumps(payload))

        ### Push to S3
        resp = self.pushProcessor.processForIngestion(TEMPLATE_NAME_POC, payload, True)
        return resp
    
    def pushAsdlPmc(self, payload):
        self.logger.info("pushAsdlPmc started ... : ")
        self.fileUtil.writeInFileWithCounter("pushAsdlPmc-input.json", json.dumps(payload))

        ### Push to S3
        resp = self.pushProcessor.processForIngestion(TEMPLATE_NAME_ASDL_PMC, payload, True)
        return resp
