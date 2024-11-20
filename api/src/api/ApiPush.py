from flask import Blueprint, jsonify, request, current_app, send_file
import os
import json
import logging
from xml.dom.minidom import Document 
import pandas as pd

from util.FileUtil import FileUtil
from apipush.PushMain import PushMain

apiPush = Blueprint('api_push', __name__)

@apiPush.route('/api/push/setupConfig', methods=['POST'])
def api_push_setupconfig():
    logging.info("welcome push setup config...")

    payload = request.get_json()

    resp = createInstancePushMain().pushSetupConfig(payload)
    return resp, 200

@apiPush.route('/api/push/poc', methods=['POST'])
def api_push_poc():
    logging.info("welcome push POC...")

    payload = request.get_json()

    resp = createInstancePushMain().pushPOC(payload)
    return resp, 200

@apiPush.route('/api/push/asdlpmc', methods=['POST'])
def api_push_asdl_pmc():
    logging.info("welcome push asdlpmc...")

    payload = request.get_json()

    resp = createInstancePushMain().pushAsdlPmc(payload)
    return resp, 200

def createInstancePushMain():
    ### FileUtil
    fileUtil = FileUtil()
    fileUtil.start()

    ### TurboMain
    configUtil = current_app.config["configUtil"]
    pushMain = PushMain(fileUtil, configUtil)

    return pushMain
