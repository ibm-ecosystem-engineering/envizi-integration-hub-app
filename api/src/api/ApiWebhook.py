from flask import Blueprint, jsonify, request, current_app
import os
import json
import logging
from xml.dom.minidom import Document 

from util.FileUtil import FileUtil
from webhook.WebhookMain import WebhookMain
from webhook.WebhookSample import WebhookSample

apiWebhook = Blueprint('api_webhook', __name__)

@apiWebhook.route('/api/webhook/loadall', methods=['POST'])
# @auth.login_required
def webhook_loadall():

    logging.info("welcome webhook_loadall...")

    configUtil = current_app.config["configUtil"]
    fileUtil = FileUtil()
    fileUtil.start()

    ### Load
    webhookMain = WebhookMain(fileUtil, configUtil)
    resp = webhookMain.loadWebhooks()

    return resp, 200

@apiWebhook.route('/api/webhook/load', methods=['POST'])
# @auth.login_required
def webhook_load():
    logging.info("welcome webhook_load...")

    configUtil = current_app.config["configUtil"]
    fileUtil = FileUtil()
    fileUtil.start()

    ### Get Payload
    payload = request.get_json()

    ### Load
    webhookMain = WebhookMain(fileUtil, configUtil)
    resp = webhookMain.loadWebhook(payload)

    return resp, 200


@apiWebhook.route('/api/webhook/load_webhook_response', methods=['POST'])
# @auth.login_required
def load_webhook_response():
    logging.info("welcome load_webhook_response...")

    configUtil = current_app.config["configUtil"]
    fileUtil = FileUtil()
    fileUtil.start()

    ### Get Payload
    payload = request.get_json()

    ### Load
    webhookMain = WebhookMain(fileUtil, configUtil)
    resp = webhookMain.load_webhook_response(payload)

    return resp, 200


@apiWebhook.route('/api/webhook/save', methods=['POST'])
# @auth.login_required
def webhook_save():
    logging.info("welcome webhook_save...")

    configUtil = current_app.config["configUtil"]
    fileUtil = FileUtil()
    fileUtil.start()

    ### Get Payload
    payload = request.get_json()

    ### Add
    webhookMain = WebhookMain(fileUtil, configUtil)
    resp = webhookMain.saveWebhook(payload)

    return resp, 200


@apiWebhook.route('/api/webhook/convert', methods=['POST'])
# @auth.login_required
def webhook_covert():
    logging.info("welcome webhook_convert...")

    configUtil = current_app.config["configUtil"]
    fileUtil = FileUtil()
    fileUtil.start()

    ### Get Payload
    payload = request.get_json()

    ### Add
    webhookMain = WebhookMain(fileUtil, configUtil)
    resp = webhookMain.convertWebhook(payload)

    return resp, 200

@apiWebhook.route('/api/webhook/add', methods=['POST'])
# @auth.login_required
def webhook_add():
    logging.info("welcome webhook_add...")

    configUtil = current_app.config["configUtil"]
    fileUtil = FileUtil()
    fileUtil.start()

    ### Get Payload
    payload = request.get_json()

    ### Add
    webhookMain = WebhookMain(fileUtil, configUtil)
    resp = webhookMain.addWebhook(payload)

    return resp, 200


@apiWebhook.route('/api/webhook/update', methods=['POST'])
# @auth.login_required
def webhook_update():
    logging.info("welcome webhook_update...")

    configUtil = current_app.config["configUtil"]
    fileUtil = FileUtil()
    fileUtil.start()

    ### Get Payload
    payload = request.get_json()

    ### Add
    webhookMain = WebhookMain(fileUtil, configUtil)
    resp = webhookMain.updateWebhook(payload)

    return resp, 200


@apiWebhook.route('/api/webhook/delete', methods=['POST'])
# @auth.login_required
def webhook_delete():
    logging.info("welcome webhook_add...")

    configUtil = current_app.config["configUtil"]
    fileUtil = FileUtil()
    fileUtil.start()

    ### Get Payload
    payload = request.get_json()

    ### Add
    webhookMain = WebhookMain(fileUtil, configUtil)
    resp = webhookMain.deleteWebhook(payload)

    return resp, 200


@apiWebhook.route('/api/webhook/execute', methods=['POST'])
# @auth.login_required
def webhook_execute():
    logging.info("welcome webhook_execute...")

    configUtil = current_app.config["configUtil"]
    fileUtil = FileUtil()
    fileUtil.start()

    ### Get Payload
    payload = request.get_json()

    ### Add
    webhookMain = WebhookMain(fileUtil, configUtil)
    resp = webhookMain.executeWebhook(payload)

    return resp, 200


@apiWebhook.route('/api/webhook/sample1', methods=['POST'])
def webhook_sample1():
    logging.info("welcome webhook_sample1...")

    configUtil = current_app.config["configUtil"]
    fileUtil = FileUtil()
    fileUtil.start()
    webhookSample = WebhookSample(fileUtil, configUtil)
    
    resp = webhookSample.sample1Webhook()

    return resp, 200

@apiWebhook.route('/api/webhook/sample2', methods=['POST'])
def webhook_sample2():
    logging.info("welcome webhook_sample2...")

    configUtil = current_app.config["configUtil"]
    fileUtil = FileUtil()
    fileUtil.start()
    webhookSample = WebhookSample(fileUtil, configUtil)

    resp = webhookSample.sample2Webhook()

    return resp, 200

@apiWebhook.route('/api/webhook/sample3', methods=['POST'])
def webhook_sample3():
    logging.info("welcome webhook_sample3...")

    configUtil = current_app.config["configUtil"]
    fileUtil = FileUtil()
    fileUtil.start()
    webhookSample = WebhookSample(fileUtil, configUtil)

    resp = webhookSample.sample3Webhook()

    return resp, 200

@apiWebhook.route('/api/webhook/sample4', methods=['POST'])
def webhook_sample4():
    logging.info("welcome webhook_sample4...")

    configUtil = current_app.config["configUtil"]
    fileUtil = FileUtil()
    fileUtil.start()
    webhookSample = WebhookSample(fileUtil, configUtil)
    
    resp = webhookSample.sample4Webhook()

    return resp, 200

@apiWebhook.route('/api/webhook/sample5', methods=['POST'])
def webhook_sample5():
    logging.info("welcome webhook_sample5...")

    configUtil = current_app.config["configUtil"]
    fileUtil = FileUtil()
    fileUtil.start()
    webhookSample = WebhookSample(fileUtil, configUtil)

    resp = webhookSample.sample5Webhook()

    return resp, 200