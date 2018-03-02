"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
from pymongo import MongoClient
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import sys

import logging

###
# Globals
###

app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY
client = MongoClient(CONFIG.MONGO_URL)
db = client.get_default_database()
collection = db['times']


###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    notes = ""
    km = request.args.get('km', 0, type=float)
    brevet = request.args.get('brevet', 200, type=int)
    if km > brevet:
        if brevet * 1.2 < km:
            notes = "Distance much longer than brevet - an accident?"
        else:
            notes = "Distance a bit longer than brevet, so used brevet"
    if km < 15:
        notes = "Distance a bit small - might cause weirdness"
    beginDate = request.args.get('beginDate', "2017-01-01", type=str)
    beginTime = request.args.get('beginTime', "00:00", type=str)
    splitBeginDate = beginDate.split("-")
    beginYear = splitBeginDate[0]
    beginMonth = splitBeginDate[1]
    beginDay = splitBeginDate[2]
    splitBeginTime = beginTime.split(":")
    beginHour = splitBeginTime[0]
    beginMin = splitBeginTime[1]
    beginTimeFinal = beginYear+"-"+beginMonth+"-"+beginDay+"T"+beginHour+":"+beginMin
    app.logger.debug("km={}".format(km))
    app.logger.debug("brevet={}".format(brevet))
    app.logger.debug("request.args: {}".format(request.args))
    open_time = acp_times.open_time(km, brevet, beginTimeFinal
    close_time = acp_times.close_time(km, brevet, beginTimeFinal)
    result = {"open": open_time, "close": close_time, "notes": notes}
    return flask.jsonify(result=result)

@app.route("/_submit_DB")
def _submit_DB():
    collection.delete_many({}) # Clear entire collection
    kms = request.args.get('kms', "", type=str).split("~")
    opens = request.args.get('opens', "", type=str).split("~")
    closes = request.args.get('closes', "", type=str).split("~")
    noteses = request.args.get('noteses', "", type=str).split("~")
    for i in range(len(kms)-1):
        collection.insert({"km": str(kms[i]), "open": opens[i], "close": closes[i], "notes": noteses[i]})
    return "fine" # Need to return something

@app.route("/_load_DB")
def _load_DB():
    data = collection.find()
    kms = []
    miles = []
    opens = []
    closes = []
    noteses = []
    for datum in data:
        if len(datum['km']) > 0: # Ignore it if it's a blank one
            kms.append(str(int(round(float(datum['km']), 0))))
            miles.append(str(round(float(datum['km']) * 0.621371, 1)))
            opens.append(datum['open'])
            closes.append(datum['close'])
            noteses.append(datum['notes'])
    result = {"kms": kms, "miles": miles, "opens": opens, "closes": closes, "noteses": noteses}
    return flask.jsonify(result=result)

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
