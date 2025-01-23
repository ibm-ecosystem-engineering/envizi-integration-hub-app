import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

import logging 
import os, json


from util.MathUtil import MathUtil

from util.DateUtils import DateUtils
from util.DictionaryUtil import DictionaryUtil
from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.ExcelUtil import ExcelUtil
from llm.LlmMain import LlmMain
from langchain_core.prompts import PromptTemplate
from docling.document_converter import DocumentConverter

class UtilityBillLlmDoclingProcessor(object):

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
        self.converter = DocumentConverter()

    def extract_data_from_pdf(self, pdf_file_name):
        result = self.converter.convert(pdf_file_name)
        markdown_output =  result.document.export_to_markdown()
        return markdown_output

    def get_prompt_templte(self) :
        prompt_template = PromptTemplate(
            input_variables=["DOCUMENT"],
            template='''
            <|start_of_role|>System<|end_of_role|> You are an AI assistant for processing invoices. Based on the provided invoice data, extract the 'Invoice Number', 'Total Net Amount', 'Total VAT or TAX or GST Amount', 'Total Amount' , 'Invoice Date', 'Purchase Order Number' and 'Customer number', without the currency values.

            |Instructions|
            Identify and extract the following information:
            - **Invoice Number**: The unique identifier for the invoice.
            - **Supplier Name**: The organization name, who created this invoice.
            - **Net Amount**: The Total Net Amount indicated on the invoice.
            - **VAT or TAX or GST Amount**: The Total VAT or TAX or GST Amount indicated on the invoice.
            - **Total Amount**: The Total Cost indicated on the invoice.
            - **Invoice Date**: The date the invoice was issued.
            - **Invoice Start Date**: The date the invoice period starts.
            - **Invoice End Date**: The date the invoice period ends.
            - **Customer Number**: The unique identifier for the customer.
            - **Customer Name**: The name of the customer.
            - **Item Description: The item description available in the invoice.
            - **Total Quantity: The total quantity in the invoice.

            Invoice Data:
            {DOCUMENT}


            Strictly provide the extracted information in the following JSON format:

            ```json
            {{
            "invoice_number": "extracted_invoice_number",
            "supplier_name": "extracted_supplier_name",
            "net_amount": "extracted_new_amount",
            "vat_or_tax_or_gst_amount" : "extracted_vat_or_tax_or_gst_amount",
            "total_amount": "extracted_total_amount",
            "invoice_date": "extracted_invoice_date",
            "invoice_start_date": "extracted_invoice_start_date",
            "invoice_end_date": "extracted_invoice_end_date",
            "customer_number": "extracted_customer_number",
            "customer_name": "extracted_customer_name",
            "item_description": "extracted_item_description",
            "total_qty": "extracted_total_quantity"

            }}

            <|end_of_text|>

            <|start_of_role|>assistant<|end_of_role|>
        ''')

        return prompt_template

    def process_utility_bills (self, folder_path):
        self.logger.debug("UtilityBillLlmDoclingProcessor : process_utility_bills ... ")

        llmMain = LlmMain(self.fileUtil, self.configUtil)

        ### Get watsonx model
        llmMain.get_watsonx_model_for_utility_bills_docling()

        ### retrieve all the files available in the bills folder
        files = self.fileUtil.retrive_image_pdf_file_names_in_folder(folder_path)

        ### Iterate files
        myList = []
        for file_name in files: 

             ### Call docling to extract the pdf content
            file_content = self.extract_data_from_pdf (file_name)

            prompt_template = self.get_prompt_templte()
            prompt = prompt_template.format(DOCUMENT=str(file_content).strip())

            ### Call watsonx.ai
            json_data = llmMain.callWatsonx_for_utility_bills_docling (prompt)

            my_supplier = DictionaryUtil.getValue_key1(json_data, "supplier_name", None)

            my_customer = DictionaryUtil.getValue_key1(json_data, "customer_number", None)
            my_startdate = DictionaryUtil.getValue_key1(json_data, "invoice_start_date", None)
            my_enddate = DictionaryUtil.getValue_key1(json_data, "invoice_end_date", None)
            my_cost = DictionaryUtil.getValue_key1(json_data, "total_amount", None)
            my_qty =  DictionaryUtil.getValue_key1(json_data, "total_qty", None)
            my_invoice_number = DictionaryUtil.getValue_key1(json_data, "invoice_number", None)

            myRow = {}
            myRow["ORGANIZATION"] = self.configUtil.ENVIZI_ORG_NAME
            myRow["Location"] = self.configUtil.UTILITY_BILL_OTHERS_LOCATION
            myRow["Account Style Caption"] = self.configUtil.UTILITY_BILL_OTHERS_ACCOUNT_STYLE
            myRow["Account Number"] = self.configUtil.ENVIZI_PREFIX + "-Utility-" + my_supplier + "-" + my_customer
            myRow["Account Reference"] = ""
            myRow["Account Supplier"] = my_supplier
            myRow["Record Start YYYY-MM-DD"] = my_startdate
            myRow["Record End YYYY-MM-DD"] =my_enddate
            myRow["Quantity"] = my_qty
            myRow["Total cost (incl. Tax) in local currency"] = my_cost
            myRow["Record Reference"] = my_customer
            myRow["Record Invoice Number"] = my_invoice_number
            myRow["Record Data Quality"] = ""
            self.logger.info("UtilityBillLlmDoclingProcessor : process_utility_bills 9 ... ")

            myList.append(myRow)

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("process_utility_bills.json", json.dumps(myList))
        self.logger.info("UtilityBillLlmDoclingProcessor : process_utility_bills 10 ... ")

        return myList
