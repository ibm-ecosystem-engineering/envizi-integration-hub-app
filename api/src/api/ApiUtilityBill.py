from flask import Blueprint, jsonify, request, current_app, send_file
import os
import json
import logging
from xml.dom.minidom import Document 

from util.FileUtil import FileUtil
from utilitybill.UtilityBillMain import UtilityBillMain

apiUtilityBill = Blueprint('api_utilitybill', __name__)

@apiUtilityBill.route('/api/utilitybill/export', methods=['POST'])
def utilitybill_export():
    logging.info("welcome utilitybill export...")

    ### Update the config data
    payload = request.get_json()

    ### FileUtil
    fileUtil = FileUtil()
    fileUtil.start()

    ### TurboMain
    configUtil = current_app.config["configUtil"]
    utilityBillMain = UtilityBillMain(fileUtil, configUtil)

    resp = utilityBillMain.exportUtilityBill()
    return resp, 200
