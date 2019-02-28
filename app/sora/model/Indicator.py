from flask import request
from rdflib import Graph, RDF, RDFS, Namespace, URIRef, Literal, BNode
from app.config import Config
import requests
import logging as log
import os
import json

class Indicator:
    def __init__(self,json_url):
        dir = os.getcwd()
        file_dir= "{}/app/sora/data/indicators.ttl".format(dir)
        self.g = Graph()
        try:
            graph = self.g.parse(file_dir, format="turtle")
        except Exception as e:

            indicator_request = requests.get(json_url)
            self.indicator_json = json.loads(indicator_request.text)

            soo = Namespace("{}sora/ontology#".format(Config.URL_ENDPOINT))
            cat = Namespace("{}sora/category#".format(Config.URL_ENDPOINT))
            qu = Namespace("https://purl.oclc.org/NET/ssnx/qu/qu#")
            m3 = Namespace("http://ontology.fiesta-iot.eu/ontologyDocs/m3-lite.owl#")

            for cat_k,cat_v in self.indicator_json.items():
                cat_name = cat_v['cat_name']
                cat_name_en = cat_v['cat_name_en']
                for k,v in cat_v['indicators'].items():
                    uri = URIRef("{}sora/indicator#{}".format(Config.URL_ENDPOINT, k))
                    uri_cat = URIRef("{}sora/category#{}".format(Config.URL_ENDPOINT, cat_k))
                    #grab the time shifts
                    url_spatial_extend = '%s?values={"ind":{"id":"%s"},"format":{"id":"raster"},"query":"getSpatialExtend"}'%(Config.URL_BACKEND_SORA, k)
                    extends_request = requests.get(url_spatial_extend)
                    extends = json.loads(extends_request.text)
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

                    for s in extends:
                        blank_node = BNode()
                        self.g.add((uri, soo.hasSpatialExtent, blank_node))
                        self.g.add((blank_node, RDF.value, Literal(s.replace("Raster ","").replace(" m",""))))
                        self.g.add((blank_node, qu.unit, m3.Metre))

                    for year in v['times'].split(","):
                        self.g.add((uri, soo.hasYearRecorded, Literal(year)))

        self.g.serialize(file_dir,format="turtle")

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




