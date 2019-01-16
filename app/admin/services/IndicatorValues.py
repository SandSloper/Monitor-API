import requests
import json

class IndicatorValues:
    def __init__(self,format):
        self.url = "https://monitor.ioer.de/backend/query.php"
        self.json = '{"format":{"id":"%s"},"query":"getAllIndicators"}' % format
        self.format=format
        req = requests.post(self.url, data={'values':self.json})
        self.values = json.loads(req.text)

    def getIndikatorValues(self,indicator_id):
        for val in self.values:
            print(val)
    #methon to return all possible indicator values which are possible for an indicator
    def getAllAvaliableServiceValues(self,service):
        res =[]
        for x in self.values:
            cat_name = self.values[x]['cat_name']
            cat_name_en = self.values[x]['cat_name_en']
            values = self.values[x]['indicators']
            ind_values = []
            for i in values:
                # if 1: the service is avaliable else not
                if int(values[i]["ogc"][service]) == 1:
                    ind_val=dict(values[i])
                    ind_id = dict({"id":i})
                    merge = dict()
                    merge.update(ind_id)
                    merge.update(ind_val)
                    del merge['atkis']
                    del merge['ogc']
                    ind_values.append(merge)

            res.append({'cat_id':x,'cat_name':cat_name,'cat_name_en':cat_name_en,"values":ind_values})

        return res