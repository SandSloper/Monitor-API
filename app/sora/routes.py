# -*- coding: utf-8 -*-
from flask import jsonify,request,Response,abort
from app.tools.toolbox import *

import requests
import json
import os

from app.sora import sora
from app.sora.request_handler import ESRIServerManager
from app.sora.model.indicator import Indicator

url = 'https://monitor.ioer.de/backend/query.php?values={"format":{"id":"raster"},"query":"getAllIndicators"}'

@sora.route("/indicator", methods=['GET', 'POST'])
def get_indicators():
    indicator = Indicator(json_url=url)
    try:
        res = indicator.g
    except Exception as e:
        return abort(500)
    if len(res) == 0:
        return abort(404)
    else:
        return Response(res.serialize(format="turtle"), mimetype="text/n3")

@sora.route("/indicator/<indicator_id>", methods=['GET', 'POST'])
def get_indicator(indicator_id):
    indicator = Indicator(json_url=url)
    try:
        query = """
                CONSTRUCT 
                {{ <http://{}/sora/indicator/{}> ?p ?o . }} 
                WHERE {{ <http://{}/sora/indicator/{}> ?p ?o. }}
                """.format(request.host,indicator_id,request.host,indicator_id)

        res = indicator.g.query(query)

    except Exception as e:
        return abort(500)
    if len(res) == 0:
        return abort(404)
    else:
        return Response(res.serialize(format="turtle"), mimetype="text/n3")

@sora.route('/services', methods=['GET', 'POST'])
def get():
    values = request.args.get('value')
    # which service is needed e.g. routing_xy or routing_poi
    job_id = request.args.get('job')
    #test if json is valid
    tb = TOOLBOX()
    if tb.json_validator(values):
        request_handler = ESRIServerManager(job_id, values)
        result = request_handler.get_request()
        response = Response(result, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Content-type'] = 'application/json; charset=utf-8'
        return response
    else:
        return jsonify(error='no valid json')

