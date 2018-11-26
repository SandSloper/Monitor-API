import requests
import json
from flask import Response

class ESRIServerManager:

    def __init__(self,job,*args, **kwargs):
        self.job = job
        self.values = kwargs.get('values',None)
        self.job_id = kwargs.get('job_id',None)
        self.jobs = {
            "routing_poi":"https://edn.ioer.de/arcgis/rest/services/SORA/routing_nearestPOI/GPServer/routing_nearestPOI",
            "routing_xy":"https://edn.ioer.de/arcgis/rest/services/SORA/routing_xy/GPServer/routing_xy",
            "coordinates":"https://edn.ioer.de/arcgis/rest/services/SORA/querybycoordinates/GPServer/querybycoordinates"
        }

    def get_request(self):
        url_submit = '{}/submitJob'.format(self.jobs[self.job])
        url_job = '{}/jobs/{}'.format(self.jobs[self.job],self.job_id)
        if self.job_id is None:
            data = {"inputJSON":self.values,"f":"pjson"}
            req = requests.post(url_submit, data=data)
        else:
            req = requests.get(url_job,params={'f': 'pjson'}, stream=True)
        print(req.url)
        result = json.loads(req.text)
        if result['jobStatus']=="esriJobSucceeded":
            param = {"f":"pjson"}
            req= requests.get("{}/{}".format(url_job,result['results']['outputJSON']['paramUrl']),stream=True, params=param)
            return Response(req.iter_content(), content_type=req.headers['content-type'])
        else:
            return Response(req.iter_content(), content_type=req.headers['content-type'])
