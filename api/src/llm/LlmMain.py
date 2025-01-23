import os

from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
import base64

import re

import requests
import json
import os
from dotenv import load_dotenv
from ibm_cloud_sdk_core import IAMTokenManager
import time

import logging 
from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.DateUtils import DateUtils

class LlmMain(object):

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

    def callWatsonx(self, project_id, model_id, prompt_input, max_new_tokens):
        self.logger.info("------------------------------------------------ callWatsonx Started ------------------------------------------------")
        start_time = time.time()
        self.logger.info(f"Prompt : {prompt_input} ")

        access_token = IAMTokenManager(apikey = self.configUtil.WATSONX_API_KEY, url =  self.configUtil.WATSONX_AUTH_URL).get_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ access_token
            }
        
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": max_new_tokens,
            "min_new_tokens": 1,
            "repetition_penalty": 1
            }
        
        llmPayload = {
            "project_id": project_id,
            "model_id": model_id, 
            "parameters": parameters,
            "input": prompt_input
            }
        
        llmResponse = requests.post(self.configUtil.WATSONX_API_URL, json=llmPayload, headers=headers)
        if llmResponse.status_code == 200:
            output = llmResponse.json()["results"][0]["generated_text"]
        else:
            output = ""

        
        end_time = time.time()
        execution_time = end_time - start_time
        self.logger.info(f"\n\n\nresult : {output} ")
        self.logger.info(f"\nExecution time: callWatsonx : {execution_time} seconds")
        self.logger.debug("------------------------------------------------ callWatsonx Completed ------------------------------------------------\n\n\n")

        return output


    def generateInvoiceSummary(self, invoiceText):
        self.logger.info("LlmMain -> generateInvoiceSummary  ... ")
        self.logger.debug(f"LlmMain -> generateInvoiceSummary  invoiceText : {invoiceText} ")

        if (invoiceText is None or invoiceText == "") :
            generated_response = ""
        else :
            # prompt_input = """You are legal expert in reviewing property title reports. \nBelow is extract of the title search report for a property.\nPlease extract the names of all the previous and current owners of the property and display these names in a numbered list in a chronological order. \nPlease ensure that you consider joint ownership and display them as single numbered item.\nPlease consider only ownership rights to the property and do not consider any person who may have other rights to the property.\n\nTitle search report:\n\n
            prompt_input = "Given below the invoice content. Can you create a nice summary out of it\n\n"

            prompt_input += " Invoice Content : " + invoiceText

            SKIP_LLM = os.getenv("SKIP_LLM", "FALSE")
            if (SKIP_LLM == "TRUE") :
                generated_response = "This a test message"
            else :
                generated_response = self.callWatsonx(self.configUtil.WATSONX_PROJECT_ID, self.configUtil.INVOICE_WATSONX_MODEL_ID, prompt_input, 200)
        return generated_response


    def get_watsonx_model_for_utility_bills(self):
        self.logger.info("------------------------------------------------ get_watsonx_model_for_utility_bills Started ------------------------------------------------")
        start_time = time.time()

        credentials = Credentials(
            url = self.configUtil.WATSONX_CREDENTIALS_URL,
            api_key = self.configUtil.WATSONX_API_KEY,
        )

        # my_params =  {
        #     GenParams.DECODING_METHOD: 'greedy',
        #     GenParams.TEMPERATURE: 2,
        #     GenParams.MIN_NEW_TOKENS: 1,
        #     GenParams.MAX_NEW_TOKENS: 512,
        #     GenParams.REPETITION_PENALTY:1.0
        # }

        my_params =  {
            # GenParams.DECODING_METHOD: 'greedy',
            GenParams.TEMPERATURE: 1,
            GenParams.MIN_NEW_TOKENS: 1,
            # GenParams.MAX_NEW_TOKENS: 512,
            GenParams.REPETITION_PENALTY:1.0
        }


        model = ModelInference(
            model_id = self.configUtil.UTILITY_BILL_LLM_MODEL_ID,
            credentials = credentials,
            project_id = self.configUtil.WATSONX_PROJECT_ID,
            params = my_params
        )

        end_time = time.time()
        execution_time = end_time - start_time
        self.logger.info(f"\nExecution time: get_watsonx_model_for_utility_bills : {execution_time} seconds")
        self.logger.debug("------------------------------------------------ get_watsonx_model_for_utility_bills Completed ------------------------------------------------\n\n\n")

        return model

    def callWatsonx_for_utility_bills(self, model, file_name, question):
        self.logger.info("------------------------------------------------ callWatsonx_for_utility_bills Started ------------------------------------------------")
        start_time = time.time()
        self.logger.info(f"\nquestion : {question}")
        self.logger.info(f"\nfile_name : {file_name}")

        ### Create base64 file
        with open(file_name, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        ### Prompt
        messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": question
                },
                {
                    "type": "image_url",
                    "image_url": {
                    "url": "data:image/jpeg;base64," + encoded_string,
                    }
                }
            ]
        }
        ]

        ### call watsonx
        response = ""
        response = model.chat(messages=messages)

        self.logger.info(f"\n\n\response : {response} ")

        try:
            result = response["choices"][0]["message"]["content"]
        except Exception as e:
             result = ""

        end_time = time.time()
        execution_time = end_time - start_time
        self.logger.info(f"\n\n\nresult : {result} ")

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("llm-output.json", json.dumps(result))

        self.logger.info(f"\nExecution time: callWatsonx_for_utility_bills : {execution_time} seconds")
        self.logger.debug("------------------------------------------------ callWatsonx_for_utility_bills Completed ------------------------------------------------\n\n\n")

        return result
    
    def get_watsonx_model_for_utility_bills_docling(self):
        self.logger.info("------------------------------------------------ get_watsonx_model_for_utility_bills_docling Started ------------------------------------------------")
        start_time = time.time()

        self.llm = WatsonxLLM(
            model_id = self.configUtil.UTILITY_BILL_DOCLING_MODEL_ID,
            apikey=self.configUtil.WATSONX_API_KEY,
            project_id=self.configUtil.WATSONX_PROJECT_ID,
            params={
                "decoding_method": "greedy",
                "max_new_tokens": 8000,
                "min_new_tokens": 1,
                "repetition_penalty": 1.01
            },
            url=self.configUtil.WATSONX_CREDENTIALS_URL
        )

        end_time = time.time()
        execution_time = end_time - start_time
        self.logger.info(f"\nExecution time: get_watsonx_model_for_utility_bills : {execution_time} seconds")
        self.logger.debug("------------------------------------------------ get_watsonx_model_for_utility_bills_docling Completed ------------------------------------------------\n\n\n")


    def callWatsonx_for_utility_bills_docling(self, prompt):
        self.logger.info("------------------------------------------------ callWatsonx_for_utility_bills_docling Started ------------------------------------------------")
        start_time = time.time()

        answer = self.llm.invoke(prompt)

        json_string = re.search(r'\{.*\}', answer, re.DOTALL).group(0).replace('\n', '')
        json_data = json.loads(json_string)

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("json_converted.json", json_string)

        end_time = time.time()
        execution_time = end_time - start_time
        self.logger.info(f"\nExecution time: callWatsonx_for_utility_bills_docling : {execution_time} seconds")
        self.logger.debug("------------------------------------------------ callWatsonx_for_utility_bills_docling Completed ------------------------------------------------\n\n\n")

        return json_data