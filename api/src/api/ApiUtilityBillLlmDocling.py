from flask import Blueprint, jsonify, request, current_app, send_file
import os
import json
import logging
from xml.dom.minidom import Document 

from util.FileUtil import FileUtil
from utilitybill_llm_docling.UtilityBillLlmDoclingMain import UtilityBillLlmDoclingMain

apiUtilityBillLlmDocling = Blueprint('api_utilitybill-llmdocling', __name__)
# apiUtilityBillLlm = Blueprint('api_utilitybill-llm', __name__)

@apiUtilityBillLlmDocling.route('/api/utilitybill/llmdocling/ingestToEnvizi', methods=['POST'])
def utility_bill_docling_ingestToEnvizi():
    logging.info("welcome utility_bill_docling_ingestToEnvizi...")

    ### FileUtil
    fileUtil = FileUtil()
    fileUtil.start()

    ### utilityBillMain
    configUtil = current_app.config["configUtil"]
    utilityBillLlmDoclingMain = UtilityBillLlmDoclingMain(fileUtil, configUtil)

    resp = utilityBillLlmDoclingMain.ingestToEnvizi()
    return resp, 200

@apiUtilityBillLlmDocling.route('/api/utilitybill/llmdocling/viewInScreen', methods=['POST'])
def utility_bill_docling_viewInScreen():
    logging.info("welcome utility_bill_docling_viewInScreen...")

    ### FileUtil
    fileUtil = FileUtil()
    fileUtil.start()

    ### utilityBillMain
    configUtil = current_app.config["configUtil"]
    utilityBillLlmDoclingMain = UtilityBillLlmDoclingMain(fileUtil, configUtil)

    resp = utilityBillLlmDoclingMain.viewInScreen()
    return resp, 200

