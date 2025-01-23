from flask import Blueprint, jsonify, request, current_app, send_file
import os
import json
import logging
from xml.dom.minidom import Document 

from util.FileUtil import FileUtil
from utilitybill.UtilityBillMain import UtilityBillMain

apiUtilityBill = Blueprint('api_utilitybill', __name__)

@apiUtilityBill.route('/api/utilitybill/ingestToEnvizi', methods=['POST'])
def utility_bill_discovery_ingestToEnvizi():
    logging.info("welcome utility_bill_discovery_ingestToEnvizi...")

    ### FileUtil
    fileUtil = FileUtil()
    fileUtil.start()

    ### utilityBillMain
    configUtil = current_app.config["configUtil"]
    utilityBillMain = UtilityBillMain(fileUtil, configUtil)

    resp = utilityBillMain.ingestToEnvizi()
    return resp, 200

@apiUtilityBill.route('/api/utilitybill/viewInScreen', methods=['POST'])
def utility_bill_discovery_viewInScreen():
    logging.info("welcome utility_bill_discovery_viewInScreen ...")

    ### FileUtil
    fileUtil = FileUtil()
    fileUtil.start()

    ### utilityBillMain
    configUtil = current_app.config["configUtil"]
    utilityBillMain = UtilityBillMain(fileUtil, configUtil)

    resp = utilityBillMain.viewInScreen()
    return resp, 200


