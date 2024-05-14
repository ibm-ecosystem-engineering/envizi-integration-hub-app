from flask import Blueprint, jsonify, request, current_app
import os
import json
import logging
from xml.dom.minidom import Document 
from envizi.EnviziMain import EnviziMain

from util.FileUtil import FileUtil

apiEnvizi = Blueprint('api_envizi', __name__)

@apiEnvizi.route('/api/envizi/locations', methods=['GET'])
# @auth.login_required
def envizi_locations():

    configUtil = current_app.config["configUtil"]

    ### Write it in output file
    fileUtil = FileUtil()
    fileUtil.start()

    ### TurboMain
    enviziMain = EnviziMain(fileUtil, configUtil)

    resp = enviziMain.exportLocation()
    return resp, 200

@apiEnvizi.route('/api/envizi/accounts', methods=['GET'])
# @auth.login_required
def envizi_accounts():

    configUtil = current_app.config["configUtil"]

    ### Write it in output file
    fileUtil = FileUtil()
    fileUtil.start()

    ### TurboMain
    enviziMain = EnviziMain(fileUtil, configUtil)

    resp = enviziMain.exportAccounts()
    return resp, 200