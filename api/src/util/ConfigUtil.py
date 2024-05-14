import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

from util.DateUtils import DateUtils

### Sigleton class to handle config file values.
class ConfigUtil :

    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigUtil, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self) :
        if not self.__initialized:
            self.__initialized = True
            self.value = None
        load_dotenv()
        self.couner = 0
        self.timestampString = ""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())
        ### Config file
        config_file_name = os.getenv("ENVIZI_CONFIG_FILE", "./envizi-config.json")
        self.configData = self._loadConfigFile(config_file_name)
        self._populateConfigDataInVariable()

    def update(self, payload):
        self.configData = payload
        self._populateConfigDataInVariable()
        return self.configData

    def updateForTurbo(self, payload):
        self.configData['turbo']['parameters']['start_date'] = payload['turbo']['parameters']['start_date']
        self.configData['turbo']['parameters']['end_date'] = payload['turbo']['parameters']['end_date']
        self._populateConfigDataInVariable()
        return self.configData

    def getConfigData(self):
        return self.configData
    

    def _loadConfigFile(self, fileName):

        data = {}
        try:
            with open(fileName, "r") as json_file:
                data = json.load(json_file)
                self.logger.debug(data)
        except FileNotFoundError:
            self.logger.error(f"The file '{fileName}' does not exist.")
        except json.JSONDecodeError:
            self.logger.error(f"The file '{fileName}' is not valid JSON.")
        return data
    
    def _populateConfigDataInVariable(self):
        self.TURBO_URL = self.configData['turbo']['access']['url']
        self.TURBO_USER = self.configData['turbo']['access']['user']
        self.TURBO_PASSWORD = self.configData['turbo']['access']['password']

        self.TURBO_GROUP_NAME = self.configData['turbo']['parameters']['group']
        self.TURBO_SUB_GROUP_NAME = self.configData['turbo']['parameters']['sub_group']

        self.TURBO_ACCOUNT_STYLES = self.configData['turbo']['account_styles']

        startDate = self.configData['turbo']['parameters']['start_date']
        endDate = self.configData['turbo']['parameters']['end_date']

        self.logger.error(f"Start Date {startDate}")
        self.logger.error(f"End Date {endDate}")

        self.TURBO_START_DATE = DateUtils.stringToDate(self.configData['turbo']['parameters']['start_date'])
        self.TURBO_END_DATE = DateUtils.stringToDate(self.configData['turbo']['parameters']['end_date'])

        self.ENVIZI_S3_AWS_BUCKET_NAME = self.configData['envizi']['access']['bucket_name']
        self.ENVIZI_S3_AWS_FOLDER_NAME = self.configData['envizi']['access']['folder_name']
        self.ENVIZI_S3_AWS_ACCESS_KEY = self.configData['envizi']['access']['access_key']
        self.ENVIZI_S3_AWS_SECRET_KEY = self.configData['envizi']['access']['secret_key']

        self.DISCOVERY_API_KEY = self.configData['discovery']['access']['api_key']
        self.DISCOVERY_SERVICE_URL = self.configData['discovery']['access']['service_url']
        self.DISCOVERY_PROJECT_ID = self.configData['discovery']['access']['project_id']
        self.DISCOVERY_COLLECTION_ID = self.configData['discovery']['access']['collection_ids']
        self.DISCOVERY_PROJECT_ID2 = self.configData['discovery']['access']['project_id2']
        self.DISCOVERY_COLLECTION_ID2 = self.configData['discovery']['access']['collection_ids2']
        self.DISCOVERY_COUNT= self.configData['discovery']['access']['count']

        self.DISCOVERY_UTILITY_BILL_ACCOUNT_STYLE = self.configData['discovery']['utility_bill']['account_style']
        self.DISCOVERY_UTILITY_BILL_LOCATION = self.configData['discovery']['utility_bill']['location']

        self.ENVIZI_ORG_NAME = self.configData['envizi']['parameters']['org_name']
        self.ENVIZI_ORG_LINK = self.configData['envizi']['parameters']['org_link']
        self.ENVIZI_PREFIX = self.configData['envizi']['parameters']['prefix']

        self.ENVIZI_API_URL = self.configData['envizi']['api']['url']
        self.ENVIZI_API_TOKEN = self.configData['envizi']['api']['token']


    def getAccountStyleInfo(self, account_style_name):
        result = None
        for account_style in self.TURBO_ACCOUNT_STYLES:
            if account_style['name'] == account_style_name:
                result = account_style
                break
        return result

