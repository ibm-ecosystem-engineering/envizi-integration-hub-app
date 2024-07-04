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

from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class DiscoveryHandler(object):

    def __init__(
        self,
        file1: FileUtil,
        configUtil: ConfigUtil
    ) -> None:
        self.file1 = file1
        self.configUtil = configUtil
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())
        self.init_config()

    def init_config(self):
        WD_API_KEY = self.configUtil.DISCOVERY_API_KEY
        WD_SERVICE_URL = self.configUtil.DISCOVERY_SERVICE_URL

        global discovery
        # Create client 
        try:
            authenticator = IAMAuthenticator(WD_API_KEY)
            discovery = DiscoveryV2(
                version='2020-08-30',
                authenticator=authenticator
                )
            discovery.set_service_url(WD_SERVICE_URL)
            discovery.set_disable_ssl_verification(True)

        except Exception as e:
            print("Unable to connect to discovery: {0}".format(e))

    def load_invoice_from_discovery(self):
        self.logger.info('--------------------- Load Invoice from Discovery started --------------------- >>>>> ')

        myQuestion = ""
        WD_PROJECT_ID = self.configUtil.DISCOVERY_PROJECT_ID
        WD_COLLECTION_IDS = self.configUtil.DISCOVERY_COLLECTION_ID
        WD_COUNT = self.configUtil.DISCOVERY_COUNT

        # global discovery
        self.logger.info(f' Discovery Query : {myQuestion} \n\n')
        self.logger.info('before querying')
        try:
            discovery_results = discovery.query(
                    project_id = WD_PROJECT_ID,
                    natural_language_query= myQuestion,
                    collection_ids= [WD_COLLECTION_IDS],
                    count = WD_COUNT
                ).get_result()

            self.logger.info('Querying completed')

            self.logger.info(f'Total documents : {len(discovery_results["results"])}')

            self.file1.writeInFileWithCounter("discovery-result.json", json.dumps(discovery_results["results"]))
        except Exception as e:
            self.logger.info(f' Unable to load passages from discovery : {e} \n\n')

        my_list = []

        try:
            for item in discovery_results["results"]:
                self.logger.info(f' item  -----> : {item}')
                my_item = {}
                my_item["document_id"] = DictionaryUtil.getValue_key1(item, "document_id", None)
                my_item["inv-supplier"] = DictionaryUtil.getValue_key1(item, "inv-supplier", None)
                my_item["inv-date"] = DictionaryUtil.getValue_key1(item, "inv-date", None)
                my_item["inv-total-cost"] = DictionaryUtil.getStringOrFirstIndex(DictionaryUtil.getValue_key1(item, "inv-total-cost", None))
                my_item["inv-goods"] = DictionaryUtil.geListAsString(DictionaryUtil.getValue_key1(item, "inv-goods", None))
                my_item["filename"] = DictionaryUtil.getValue_key2(item, "extracted_metadata", "filename", None)
                my_item["text"] = DictionaryUtil.getStringOrFirstIndex(DictionaryUtil.getValue_key1(item, "text", None))
                my_list.append(my_item)

            self.file1.writeInFileWithCounter("result.json", json.dumps(my_list))
        except Exception as e:
            self.logger.info(f' Unable to process discovery result : {e} \n\n')

        result = {}
        result["result"] = my_list 
        self.logger.info(' <<<<< --------------------- Load Invoice from Discovery completed --------------------- ')
        return result
    

    def load_utility_from_discovery(self):
        self.logger.info('--------------------- Load Utility from Discovery started --------------------- >>>>> ')

        myQuestion = ""
        WD_PROJECT_ID = self.configUtil.DISCOVERY_PROJECT_ID2
        WD_COLLECTION_IDS = self.configUtil.DISCOVERY_COLLECTION_ID2
        WD_COUNT = self.configUtil.DISCOVERY_COUNT

        # global discovery
        self.logger.info(f' Discovery Query : {myQuestion} \n\n')
        self.logger.info('before querying')
        try:
            discovery_results = discovery.query(
                    project_id = WD_PROJECT_ID,
                    natural_language_query= myQuestion,
                    collection_ids= [WD_COLLECTION_IDS],
                    count = WD_COUNT
                ).get_result()

            self.logger.info('Querying completed')

            self.logger.info(f'Total documents : {len(discovery_results["results"])}')

            self.file1.writeInFileWithCounter("discovery-result.json", json.dumps(discovery_results["results"]))
        except Exception as e:
            self.logger.info(f' Unable to load passages from discovery : {e} \n\n')

        my_list = []

        try:
            for item in discovery_results["results"]:
                self.logger.info(f' item  -----> : {item}')
                my_item = {}
                my_item["document_id"] = DictionaryUtil.getValue_key1(item, "document_id", None)
                my_item["my_supplier"] = DictionaryUtil.getValue_key1(item, "my_supplier", None)
                my_item["my_customer"] = DictionaryUtil.getValue_key1(item, "my_customer", None)
                my_item["my_cost"] = DictionaryUtil.getValue_key1(item, "my_cost", None)
                my_item["my_startdate"] = DictionaryUtil.getValue_key1(item, "my_startdate", None)
                my_item["my_enddate"] = DictionaryUtil.getValue_key1(item, "my_enddate", None)
                my_item["my_qty"] = DictionaryUtil.getValue_key1(item, "my_qty", None)
                my_item["my_customer"] = DictionaryUtil.getValue_key1(item, "my_customer", None)
                my_item["filename"] = DictionaryUtil.getValue_key2(item, "extracted_metadata", "filename", None)
                my_item["text"] = DictionaryUtil.getStringOrFirstIndex(DictionaryUtil.getValue_key1(item, "text", None))
                my_list.append(my_item)
            self.file1.writeInFileWithCounter("result.json", json.dumps(my_list))
        except Exception as e:
            self.logger.info(f' Unable to process discovery result : {e} \n\n')

        result = {}
        result["result"] = my_list 
        self.logger.info(' <<<<< --------------------- Load Utility from Discovery completed --------------------- ')
        return result    