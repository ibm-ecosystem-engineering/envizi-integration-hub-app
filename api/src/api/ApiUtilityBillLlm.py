from flask import Blueprint, jsonify, request, current_app, send_file
import os
import json
import logging
from xml.dom.minidom import Document 

from util.FileUtil import FileUtil
from utilitybill_llm.UtilityBillLlmMain import UtilityBillLlmMain

apiUtilityBillLlm = Blueprint('api_utilitybill-llm', __name__)

@apiUtilityBillLlm.route('/api/utilitybill/llm/ingestToEnvizi', methods=['POST'])
def utility_bill_ingestToEnvizi():
    logging.info("welcome utility_bill_ingestToEnvizi...")

    ### FileUtil
    fileUtil = FileUtil()
    fileUtil.start()

    ### utilityBillMain
    configUtil = current_app.config["configUtil"]
    utilityBillLlmMain = UtilityBillLlmMain(fileUtil, configUtil)

    resp = utilityBillLlmMain.ingestToEnvizi()
    return resp, 200

@apiUtilityBillLlm.route('/api/utilitybill/llm/viewInScreen', methods=['POST'])
def utility_bill_viewInScreen():
    logging.info("welcome utility_bill_viewInScreen...")

    ### FileUtil
    fileUtil = FileUtil()
    fileUtil.start()

    ### utilityBillMain
    configUtil = current_app.config["configUtil"]
    utilityBillLlmMain = UtilityBillLlmMain(fileUtil, configUtil)

    resp = utilityBillLlmMain.viewInScreen()
    return resp, 200

