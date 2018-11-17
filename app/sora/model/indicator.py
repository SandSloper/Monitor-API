from flask import request
from rdflib import Graph, RDF, RDFS, Namespace, BNode, URIRef, Literal
from rdflib.plugins.sparql.results.jsonresults import JSONResultSerializer
from requests import get
import logging as log
from io import StringIO
import json

class Indicator:
    def __init__(self,json=None, json_url=None):
        if not json is None:
            indicator_json = json
        else:
            indicator_json = get(json_url).json()

        soo = Namespace("http://{}/sora/ontology#".format(request.host))
        qu = Namespace("http://purl.oclc.org/NET/ssnx/qu/qu#")
        self.g = Graph()

        for x in indicator_json.values():
            for k,v in x['indicators'].items():
                uri = URIRef("http://{}/sora/indicator/{}".format(request.host,k))
                #create the graph
                self.g.add((uri, RDF.type, soo.Indicator))
                self.g.add((uri, soo.hasIndicatorId, Literal(k)))
                self.g.add((uri, RDFS.label, Literal(v['ind_name'], lang='de')))
                self.g.add((uri, RDFS.label, Literal(v['ind_name_en'], lang='en')))

                self.g.add((uri, soo.interpretation, Literal(v['interpretation'], lang='de')))
                self.g.add((uri, soo.interpretation, Literal(v['interpretation_en'], lang='en')))

                self.g.add((uri, soo.methodology, Literal(v['methodik'], lang='de')))
                self.g.add((uri, soo.methodology, Literal(v['methodology'], lang='en')))

                self.g.add((uri, qu.Unit, Literal(v['unit'])))

                for year in v['times'].split(","):
                    self.g.add((uri, soo.hasYearRecorded, Literal(year)))

    def sparql(self, query):

        try:
            res = self.g.query(query)
            json_result = res.serialize(format="json")

            log.info(str(res))
            log.info(json_result)
            return {
                'status': 'completed',
                'result': str(json_result)
            }

        except Exception as e:
            return {
                'status': 'failed',
                'result': str(e)
            }




