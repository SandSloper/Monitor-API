import requests
import json
import os

class ESRIServerManager:

    def __init__(self,job_id,values):
        self.job_id = job_id
        self.values = values
        self.jobs = {
            "routing_poi":"https://edn.ioer.de/arcgis/rest/services/SORA/routing_nearestPOI/GPServer/routing_nearestPOI/execute",
            "routing_xy":"https://edn.ioer.de/arcgis/rest/services/SORA/routing_xy/GPServer/routing_xy/execute",
            "coordinates":"https://edn.ioer.de/arcgis/rest/services/SORA/querybycoordinates/GPServer/querybycoordinates/execute"
        }

    def get_request(self):
        req = requests.post(self.jobs[self.job_id],data=self.values,params={'f':'pjson'})
        print(req.text)
        resultJSON = json.loads(req.text)
        values = None
        for x in resultJSON['results']:
           values =  x['value']
        return json.dumps(values)