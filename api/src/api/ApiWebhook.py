from flask import Blueprint, jsonify, request, current_app
import os
import json
import logging
from xml.dom.minidom import Document 

from util.FileUtil import FileUtil
from webhook.WebhookMain import WebhookMain
from webhook.WebhookSample import WebhookSample

apiWebhook = Blueprint('api_webhook', __name__)

def createInstanceWebhookMain():
    ### FileUtil
    fileUtil = FileUtil()
    fileUtil.start()

    ### TurboMain
    configUtil = current_app.config["configUtil"]
    webhookMain = WebhookMain(fileUtil, configUtil)

    return webhookMain


@apiWebhook.route('/api/webhook/loadall', methods=['POST'])
# @auth.login_required
def webhook_loadall():

    logging.info("welcome webhook_loadall...")

    ### Load
    resp = createInstanceWebhookMain().loadWebhooks()

    return resp, 200

@apiWebhook.route('/api/webhook/load', methods=['POST'])
# @auth.login_required
def webhook_load():
    logging.info("welcome webhook_load...")

    ### Get Payload
    payload = request.get_json()

    ### Load
    resp = createInstanceWebhookMain().loadWebhook(payload)

    return resp, 200

@apiWebhook.route('/api/webhook/loadnew', methods=['POST'])
# @auth.login_required
def webhook_loadnew():
    logging.info("welcome webhook_loadnew...")

    ### Get Payload
    payload = request.get_json()

    ### Load
    resp = createInstanceWebhookMain().loadWebhookNew(payload)

    return resp, 200

@apiWebhook.route('/api/webhook/templatechange', methods=['POST'])
def webhook_templatechange():
    logging.info("welcome webhook_templatechange...")

    ### Get Payload
    payload = request.get_json()

    ### Load
    resp = createInstanceWebhookMain().loadWebhookTemplateChange(payload)

    return resp, 200

@apiWebhook.route('/api/webhook/load_webhook_response', methods=['POST'])
# @auth.login_required
def load_webhook_response():
    logging.info("welcome load_webhook_response...")

    ### Get Payload
    payload = request.get_json()

    ### Load
    resp = createInstanceWebhookMain().load_webhook_response(payload)

    return resp, 200


@apiWebhook.route('/api/webhook/save', methods=['POST'])
# @auth.login_required
def webhook_save():
    logging.info("welcome webhook_save...")

    ### Get Payload
    payload = request.get_json()

    ### Add
    resp = createInstanceWebhookMain().saveWebhook(payload)

    return resp, 200


@apiWebhook.route('/api/webhook/ingestToEnvizi', methods=['POST'])
# @auth.login_required
def webhook_ingestToEnvizi():
    logging.info("welcome webhook_ingestToEnvizi...")

    ### Get Payload
    payload = request.get_json()

    ### Add
    resp = createInstanceWebhookMain().ingestToEnvizi(payload)

    return resp, 200

@apiWebhook.route('/api/webhook/viewInScreen', methods=['POST'])
# @auth.login_required
def webhook_viewInScreen():
    logging.info("welcome webhook_viewInScreen...")

    ### Get Payload
    payload = request.get_json()

    ### Add
    resp = createInstanceWebhookMain().viewInScreen(payload)

    return resp, 200

@apiWebhook.route('/api/webhook/add', methods=['POST'])
# @auth.login_required
def webhook_add():
    logging.info("welcome webhook_add...")

    ### Get Payload
    payload = request.get_json()

    ### Add
    resp = createInstanceWebhookMain().addWebhook(payload)

    return resp, 200


@apiWebhook.route('/api/webhook/update', methods=['POST'])
# @auth.login_required
def webhook_update():
    logging.info("welcome webhook_update...")

    ### Get Payload
    payload = request.get_json()

    ### Add
    resp = createInstanceWebhookMain().updateWebhook(payload)

    return resp, 200


@apiWebhook.route('/api/webhook/delete', methods=['POST'])
# @auth.login_required
def webhook_delete():
    logging.info("welcome webhook_add...")

    ### Get Payload
    payload = request.get_json()

    ### Add
    resp = createInstanceWebhookMain().deleteWebhook(payload)

    return resp, 200

@apiWebhook.route('/api/webhook/sample', methods=['POST'])
def webhook_sample():
    logging.info("welcome webhook_sample...")

    configUtil = current_app.config["configUtil"]
    fileUtil = FileUtil()
    fileUtil.start()
    webhookSample = WebhookSample(fileUtil, configUtil)
    
    ### Get Payload
    name = request.args.get('name')

    resp = webhookSample.sampleWebhook(name)

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