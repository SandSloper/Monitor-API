from flask import request
from rdflib import Graph, RDF, RDFS, Namespace, URIRef, Literal
from requests import get
import logging as log

class Indicator:
    def __init__(self,json=None, json_url=None):
        if not json is None:
            indicator_json = json
        else:
            indicator_json = get(json_url).json()

        soo = Namespace("https://{}/monitor_api/sora/ontology#".format(request.host))
        cat = Namespace("https://{}/monitor_api/sora/category#".format(request.host))
        qu = Namespace("https://purl.oclc.org/NET/ssnx/qu/qu#")
        self.g = Graph()

        for cat_k,cat_v in indicator_json.items():
            cat_name = cat_v['cat_name']
            cat_name_en = cat_v['cat_name_en']
            for k,v in cat_v['indicators'].items():
                uri = URIRef("https://{}/monitor_api/sora/indicator#{}".format(request.host,k))
                uri_cat = URIRef("https://{}/monitor_api/sora/category#{}".format(request.host,cat_k))
                #create the graph
                self.g.add((uri, RDF.type, soo.Indicator))
                self.g.add((uri, soo.hasCategory, uri_cat))
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




