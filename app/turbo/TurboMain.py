import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

import logging 
import os, json

from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from turbo.TurboProcessor import TurboProcessor

class TurboMain(object):

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
        self.turboProcessor = TurboProcessor(self.fileUtil, self.configUtil)

    def queryForIngest(self, payload):
        resp = self.queryForIntegration(payload, True)
        return resp
    
    def queryForView(self, payload):
        resp = self.queryForIntegration(payload, False)
        return resp

    def queryForIntegration(self, payload, ingestFlag):
        self.fileUtil.writeInFileWithCounter("payload.json", json.dumps(payload))

        ### Update param for Turbo
        self.configUtil.updateForTurbo(payload)

        self.logger.debug(f" TURBO_START_DATE : {self.configUtil.TURBO_START_DATE}")
        self.logger.debug(f" TURBO_END_DATE : {self.configUtil.TURBO_END_DATE}")

        ### Turbo login
        sessionid = self.turboProcessor.turboLogin(payload)

        ### Group and Locations
        self.turboProcessor.queryTurboRegion(payload, sessionid)
        dataCenterJson = self.turboProcessor.queryTurboDataCenter(payload, sessionid)
        myLocationData = self.turboProcessor.createLocationData(dataCenterJson)
        locationsFile = self.turboProcessor.writeDataInS3(myLocationData, "Locations", "Setup", "Envizi_SetupConfig_", ingestFlag)

        ### Accounts and Data
        myAccountsData = self.turboProcessor.queryTurboForAccounts(payload, sessionid, self.configUtil.TURBO_START_DATE, self.configUtil.TURBO_END_DATE)
        accountsFile = self.turboProcessor.writeDataInS3(myAccountsData, "Accounts", "Records to load", "POC Account Setup and Data Load_", ingestFlag)

        resp = {"locationData": myLocationData, 
                "accountsData": myAccountsData, 
                "inputPayload": payload, 
                "locationsFile": locationsFile, 
                "accountsFile": accountsFile,
                "result": "sucess"}

        return resp