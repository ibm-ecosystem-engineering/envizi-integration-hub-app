from flask import Blueprint, jsonify, request, current_app
import os
import json
import logging
from xml.dom.minidom import Document 

from util.FileUtil import FileUtil

apiConfig = Blueprint('api_config', __name__)

@apiConfig.route('/api/config/load', methods=['POST'])
def config_load():

    configUtil = current_app.config["configUtil"]
    resp = configUtil.getConfigData()

    ### Write it in output file
    fileUtil = FileUtil()
    fileUtil.start()
    fileUtil.writeInFileWithCounter("envizi-config.json", json.dumps(resp))

    return resp, 200


@apiConfig.route('/api/config/update', methods=['POST'])
def config_update():

    configUtil = current_app.config["configUtil"]

    ### Write current data in ouput file
    fileUtil = FileUtil()
    fileUtil.start()
    fileUtil.writeInFileWithCounter("envizi-config_prev.json", json.dumps(configUtil.getConfigData()))

    ### Update the config data
    payload = request.get_json()
    resp = configUtil.update(payload)

    ### Write updated config data in ouput file
    fileUtil.writeInFileWithCounter("envizi-config_new.json", json.dumps(configUtil.getConfigData()))

    return resp, 200