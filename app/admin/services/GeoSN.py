# -*- coding: utf-8 -*-
import datetime
import os

from app import app
from app.admin.interfaces.GeoSnService import GeoSnService
import xmltodict

# ToDo Weblaufwerk: https://monitor.ioer.de/ogc/  -> von Jörg erstellt auf Server ist es der Pfad: /srv/www/htdocs/monitor_ogc_xml/
from app.admin.models.IoerIndicator import IoerIndicator
from app.admin.models.Toolbox import Toolbox
from app.admin.services.IndicatorValues import IndicatorValues

class GeoSN(GeoSnService):
    indicator = None

    def __init__(self, _path='/srv/www/htdocs/monitor_ogc_xml/'):
        self.path = _path
        self.toolbox = Toolbox()

    def update(self):
        results = []
        ind_values = IndicatorValues('raster')
        #the raster value
        wcs_values = ind_values.getAllAvaliableServiceValues("wcs")
        #the wfs values
        wfs_values = ind_values.getAllAvaliableServiceValues("wfs")
        for x in wfs_values:
            values = x['values']
            # get the possible rster extends
            for val in values:
                ind_id = val["id"]
                ind_name = val['ind_name']
                ind_description = val['interpretation'].replace('"', "'").replace("\n", "")
                times = val["times"]
                methodology = self.toolbox.clean_string(val["methodik"])
                unit = val["unit"]
                # builder
                self.indicator = IoerIndicator(ind_id, ind_name, ind_description, times, "WFS", unit, methodology)
                results.append(self.__updateFile("wfs"))


        for w in wcs_values:
            values = w['values']
            # get the possible rster extends
            for val in values:
                ind_id = val["id"]
                ind_name = val['ind_name']
                ind_description = val['interpretation'].replace('"', "'").replace("\n", "")
                times = val["times"]
                methodology = self.toolbox.clean_string(val["methodik"])
                unit = val["unit"]
                # builder
                self.indicator = IoerIndicator(ind_id, ind_name, ind_description, times, "WMS/WCS", unit, methodology)
                results.append(self.__updateFile("wms"))
                results.append(self.__updateFile("wcs"))

        return results

    #private function
    def __updateFile(self, service):
        indicator_set = self.indicator
        file = os.path.join(self.path, "{}_{}.xml".format(indicator_set.get_id(),service))
        app.logger.debug(file)
        print(file)
        # Todo nach Id parsen und diese erst verwenden wenn die URL überenstimmen
        try:
            with open(file,"r",encoding="utf-8") as fr:
                doc = xmltodict.parse(fr.read().replace("&","&amp;"))
                fr.close()
                # set the time stamp
                now = datetime.datetime.now()
                doc["gmd:MD_Metadata"]["gmd:dateStamp"]["gco:Date"] =now.strftime("%Y-%m-%d")
                # set the indicator values
                doc_ind = doc["gmd:MD_Metadata"]["gmd:identificationInfo"]["srv:SV_ServiceIdentification"]
                doc_ind["gmd:citation"]["gmd:CI_Citation"]["gmd:title"]["gco:CharacterString"]="{} {}".format(service.upper(), indicator_set.get_name())
                doc_ind["gmd:citation"]["gmd:CI_Citation"]["gmd:date"]["gmd:CI_Date"]["gmd:date"]["gco:date"]=now.strftime("%Y-%m-%d")
                doc_ind["gmd:abstract"]["gco:CharacterString"] = "{} Weitere Informationen unter http://www.ioer-monitor.de/index.php?id=44&ID_IND={}".format(indicator_set.get_description(),indicator_set.get_id())
                # set the operations
                doc_op =  doc["gmd:MD_Metadata"]["gmd:identificationInfo"]["srv:SV_ServiceIdentification"]["srv:containsOperations"]
                # parse for the urls and update them
                for op in doc_op:
                    # extract id from the url
                    node_op = op["srv:SV_OperationMetadata"]["srv:operationName"]["gco:CharacterString"].get("#text")
                    url = "https://monitor.ioer.de/cgi-bin/{}?MAP={}_{}".format(service,indicator_set.get_id(),service)
                    #build get capabilities URL
                    if node_op == 'GetCapabilities':
                        url = "{}&service={}&VERSION=2.0.0&REQUEST=GetCapabilities".format(url,service)

                    op["srv:SV_OperationMetadata"]["srv:connectPoint"]["gmd:CI_OnlineResource"]["gmd:linkage"]["gmd:URL"] = url

            with open(file, "w",encoding="utf-8") as fw:
                out = xmltodict.unparse(doc, pretty=True)
                fw.write(out.replace("&amp;","&"))
                fw.close()
                app.logger.debug("Update Service for {}".format("https://monitor.ioer.de/cgi-bin/{}?MAP={}_{}".format(service,indicator_set.get_id(),service)))

            return self.indicator.toJSON()

        except IOError as e:
            app.logger.debug("Missing service for: {}&service={}&VERSION=2.0.0&REQUEST=GetCapabilities".format( "https://monitor.ioer.de/cgi-bin/{}?MAP={}_{}".format(service,indicator_set.get_id(),service),service))
            return self.indicator.toJSON("I/O error({0})".format(e))