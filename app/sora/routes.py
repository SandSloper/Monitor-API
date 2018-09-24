# -*- coding: utf-8 -*-
from flask import jsonify,request,Response
from rdflib import Graph,URIRef, BNode, Literal
from rdflib.namespace import RDF

import requests
import json
import os


from app.sora import sora
from app.sora.request_handler import ESRIServerManager

@sora.route('/rdf')
def rdf():
    # get all avalibable indicators from the server
    url='https://monitor.ioer.de/monitor_test/backend/query.php'
    json_string = '{"format":{"id":"raster"},"query":"getAllIndicators"}'
    req = requests.get("{}".format(url,json_string))
    categories = json.loads(req.text)
    # create the graph for the RDF DOC
    # siehe Lars: https://git.gesis.org/SoRa/sora-app/blob/master/backend/project/resources/indicator.py
    g = Graph()
    indicator = URIRef("http://monitor.ioer.de:5000/ressources/indicator")
    for cat in categories:
        ind_id = categories[cat]['indicators']
        for x in ind_id:
            ind_name = categories[cat]['indicators'][x]['ind_name']

    g.serialize(destination=os.path.dirname(os.path.realpath(__file__))+'/ressources/indicator.ttl', format='turtle')

    return jsonify(True)

@sora.route('/routing_xy', methods=['GET', 'POST'])
def get():
    values = request.args.get('value')
    job_id = request.args.get('job')
    request_handler = ESRIServerManager(job_id, values)
    result = request_handler.get_request()
    return Response(result, mimetype='application/json')

