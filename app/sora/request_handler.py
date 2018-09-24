import requests
import json
import os

class ESRIServerManager:

    def __init__(self,job_id,values):
        self.job_id = job_id
        self.values = values
        self.jobs = {
            "poi":"https://edn.ioer.de/arcgis/rest/services/SORA/routing_nearestPOI/GPServer/routing_nearestPOI/execute",
            "routing_xy":"https://edn.ioer.de/arcgis/rest/services/SORA/routing_xy/GPServer/routing_xy/execute",
        }

    def get_request(self):
        request_url = "{}?inputJSON={}&f=pjson".format(self.jobs[self.job_id],self.values)
        req = requests.get(request_url)
        resultJSON = json.loads(req.text)
        values = None
        for x in resultJSON['results']:
           values =  x['value']
        print(values)
        return json.dumps(values)