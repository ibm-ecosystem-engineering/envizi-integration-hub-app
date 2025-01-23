from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS

# import getpass
import os
import logging 
from dotenv import load_dotenv

from flask_basicauth import BasicAuth
from flask_login import login_required, fresh_login_required

from api.ApiTurbo import apiTurbo
from api.ApiMisc import apiMisc
from api.ApiConfig import apiConfig
from api.ApiExcel import apiExcel
from api.ApiExcelPro import apiExcelPro
from api.ApiInvoice import apiInvoice
from api.ApiEnvizi import apiEnvizi
from api.ApiWebhook import apiWebhook
from api.ApiUtilityBill import apiUtilityBill
from api.ApiUtilityBillLlm import apiUtilityBillLlm
from api.ApiUtilityBillLlmDocling import apiUtilityBillLlmDocling

from api.ApiLogin import apiLogin
from api.ApiPush import apiPush

from util.ConfigUtil import ConfigUtil
from scheduler.SchedulerMain import SchedulerMain
from webhook.WebhookScheduler import WebhookScheduler

#### Logging Configuration
logging.basicConfig(
    format='%(asctime)s - %(levelname)s:%(message)s',
    handlers=[
        logging.StreamHandler(), #print to console
    ],
    level=logging.INFO
)

app = Flask(__name__)
# auth = HTTPBasicAuth()

CORS(app)

# auth = BasicAuth(app)

app.register_blueprint(apiTurbo)
app.register_blueprint(apiMisc)
app.register_blueprint(apiConfig)
app.register_blueprint(apiExcel)
app.register_blueprint(apiExcelPro)
app.register_blueprint(apiInvoice)
app.register_blueprint(apiEnvizi)
app.register_blueprint(apiWebhook)
app.register_blueprint(apiUtilityBill)
app.register_blueprint(apiUtilityBillLlm)
app.register_blueprint(apiUtilityBillLlmDocling)

app.register_blueprint(apiLogin)
app.register_blueprint(apiPush)

# app.config['STATIC_FOLDER'] = 'static'  # Tells Flask to use 'static' as the static folder name

# Sample user data

# @auth.verify_password
# def verify_password(username, password):
#     if username in users and users[username] == password:
#         return username

@app.route('/welcome')
def indexwelcome():
    resp = "Welcome to the Envizi Integration Hub"
    return resp, 200

@app.route('/hello')
# @auth.login_required
def indexhellow():
    resp = {"msg": "hello"}
    return resp, 200

@app.route('/')
# @auth.login_required
def index():
    return app.send_static_file('index.html')

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

# @auth.verify_password
# def verify_password(username, password):
#     if username in users and users[username] == password:
#         return username



### Main method
def init_schedulers():
    logging.info("init_schedulers started .....")

    configUtil = app.config["configUtil"]

    schedulerMain = SchedulerMain(configUtil)
    app.config["schedulerMain"] = schedulerMain

    webhookScheduler = WebhookScheduler(configUtil, schedulerMain)
    webhookScheduler.createJobsForWebhooks()

### Main method
def main():
    logging.info("main started .....")
    load_dotenv()

    # Configure basic authentication
    # app.config['BASIC_AUTH_USERNAME'] = os.getenv("APP_USERNAME", "admin")
    # app.config['BASIC_AUTH_PASSWORD'] = os.getenv("APP_PASSWORD", "admin")

    configUtil = ConfigUtil()
    app.config["configUtil"] = configUtil

    # Get all attributes of the module
    module_attributes = dir(ConfigUtil)
    # Print the list of attributes
    print(module_attributes)

    init_schedulers()

    ### Run the app
    app.run(host ='0.0.0.0', port = 3001, debug = False)

if __name__ == '__main__':
    main()

