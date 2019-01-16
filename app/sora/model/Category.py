from flask import request
from rdflib import Graph, RDF, RDFS, Namespace, URIRef, Literal
import requests
import json
import logging as log
from app.config import Config

class Category:
    def __init__(self,json_url):
        indicator_request = requests.get(json_url)
        indicator_json = json.loads(indicator_request.text)
            
        soo = Namespace("{}sora/ontology#".format(Config.URL_ENDPOINT))
        qu = Namespace("https://purl.oclc.org/NET/ssnx/qu/qu#")
        self.g = Graph()

        for k,v in indicator_json.items():
            cat_id =k
            cat_name = v['cat_name']
            cat_name_en = v['cat_name_en']
            uri = URIRef("{}sora/category#{}".format(Config.URL_ENDPOINT, cat_id))
            self.g.add((uri, soo.hasCategoryId, Literal(cat_id)))
            self.g.add((uri, RDFS.label, Literal(cat_name, lang='de')))
            self.g.add((uri, RDFS.label, Literal(cat_name_en, lang='en')))

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




