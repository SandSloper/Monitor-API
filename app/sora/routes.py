# -*- coding: utf-8 -*-
from rdflib import Graph
from flask import jsonify, request, Response, abort
import os

from app import *
from app.sora import sora
from app.sora.RequestHandler import ESRIServerManager
from app.sora.model.Indicator import Indicator
from app.sora.model.Category import Category
from app.config import Config

url = '%s?values={"format":{"id":"raster"},"query":"getAllIndicators"}' % (Config.URL_BACKEND_SORA)

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

@sora.route("/category", methods=['GET', 'POST'])
def get_categories():
    category = Category(json_url=url)
    try:
        res = category.g
    except Exception as e:
        return abort(500)
    if len(res) == 0:
        return abort(404)
    else:
        return Response(res.serialize(format="turtle"), mimetype="text/n3")

@sora.route("/ontology",methods=['GET', 'POST'])
def get_ontology():
    dir = os.getcwd()
    graph = Graph().parse("{}/app/sora/data/ontology.ttl".format(dir),format="turtle")
    response = Response(graph.serialize(format="turtle"), mimetype='text/n3')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@sora.route('/services',methods=['GET', 'POST'])
def get():
    job = request.args.get('job')
    values = request.get_data() or None
    job_id = request.args.get('job_id') or None
    # test if JSON is valid
    try:
        #validate json
        #set request and get response from esri server
        request_handler = ESRIServerManager(job, values=values,job_id=job_id)
        app.logger.debug("result: \n%s",str(request_handler.get_request()))
        return request_handler.get_request()
    except Exception as e:
        return jsonify(error=str(e))
