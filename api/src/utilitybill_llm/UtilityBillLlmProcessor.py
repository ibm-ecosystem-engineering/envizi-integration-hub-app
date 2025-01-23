import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

import requests
import logging 
import os, json


from util.MathUtil import MathUtil

from util.DateUtils import DateUtils
from util.DictionaryUtil import DictionaryUtil
from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.ExcelUtil import ExcelUtil
from llm.LlmMain import LlmMain

class UtilityBillLlmProcessor(object):

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


    def process_utility_bills (self, folder_path):

        llmMain = LlmMain(self.fileUtil, self.configUtil)

        ### Get watsonx model
        model = llmMain.get_watsonx_model_for_utility_bills()

        ### retrieve all the files available in the bills folder
        files = self.fileUtil.retrive_image_pdf_file_names_in_folder(folder_path)

        ### Iterate files
        myList = []
        for file_name in files: 
            
            prompt_template_default = """
                Your task is to answer question accurately. Follow these rules:
                1. Only use the information in the image to answer.
                2. If the answer is not explicitly stated in the image content, respond with "Nil" and don't give any reasons or explanations
                3. Provide only the exact value without any additional text. You don't need to give explanation for your answer.

                Question : 
                """

            question = prompt_template_default + "What is the billing start date ?"
            my_startdate = llmMain.callWatsonx_for_utility_bills (model, file_name, question)
            my_startdate = DateUtils.convert_any_date_format_to_YYYYMMDD(my_startdate)

            question = prompt_template_default + "What is the billing end date ?"
            my_enddate = llmMain.callWatsonx_for_utility_bills (model, file_name, question)
            my_enddate = DateUtils.convert_any_date_format_to_YYYYMMDD(my_enddate)

            question = prompt_template_default + "Provide the billing amount from the given utility bill."
            my_cost = llmMain.callWatsonx_for_utility_bills (model, file_name, question)

            question = prompt_template_default + "Extract the total units/qty consumed from the given utility bill."
            my_qty = llmMain.callWatsonx_for_utility_bills (model, file_name, question)

            question = prompt_template_default + "Which company is the bill from?"
            my_supplier = llmMain.callWatsonx_for_utility_bills (model, file_name, question)

            question = prompt_template_default + "What is the account number , customer number or customer name of this bill?"
            my_customer = llmMain.callWatsonx_for_utility_bills (model, file_name, question)

            myRow = {}
            myRow["ORGANIZATION"] = self.configUtil.ENVIZI_ORG_NAME
            myRow["Location"] = self.configUtil.UTILITY_BILL_OTHERS_LOCATION
            myRow["Account Style Caption"] = self.configUtil.UTILITY_BILL_OTHERS_ACCOUNT_STYLE
            myRow["Account Number"] = self.configUtil.ENVIZI_PREFIX + "-Utility-" + my_supplier + "-" + my_customer
            myRow["Account Reference"] = ""
            myRow["Account Supplier"] = my_supplier
            myRow["Record Start YYYY-MM-DD"] = my_startdate
            myRow["Record End YYYY-MM-DD"] = my_enddate
            myRow["Quantity"] = my_qty
            myRow["Total cost (incl. Tax) in local currency"] = my_cost
            myRow["Record Reference"] = my_customer
            myRow["Record Invoice Number"] = ""
            myRow["Record Data Quality"] = ""

            myList.append(myRow)

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("process_utility_bills.json", json.dumps(myList))

        return myList
