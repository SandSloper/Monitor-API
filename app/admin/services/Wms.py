# -*- coding: utf-8 -*-
import os
import codecs
import requests
import json
import datetime
import csv

from app import *
from app.config import Config
from app.models.Toolbox import Toolbox
from app.admin.models.Color import Color
from app.admin.models.IndicatorValues import IndicatorValues
from app.admin.models.Indicator import Indicator
from app.admin.interfaces.OgcService import OgcService

'''
Info: Raster werden nur noch in der Rasterweite 100m angeboten oder in der am geringsten vorliegenden 
'''

class Wms(OgcService):
    indicator = None
    def __init__(self,path='/mapsrv_daten/detailviewer/wms_mapfiles'):
        self.service = 'wms'
        self.path = path
        self.toolbox = Toolbox()

    def getQuantil(self, id, width, year):
        quantile = []
        #server path
        #quantile_path = "data/{0}/Raster {1} m/r{1}_{0}_{2}_quantile.txt".format(year,width,id)
        quantile_path = "data\\{0}\\Raster {1} m\\r{1}_{0}_{2}_quantile.txt".format(year, width, id)
        if "wms_mapfiles" in self.path:
            path = self.path.replace("wms_mapfiles", quantile_path)
        elif "wms_monitor" in self.path:
            path = self.path.replace("wms_monitor", quantile_path)
        try:
            with open(path) as quantile_csv:
                csv_reader = csv.reader(quantile_csv,delimiter=";")
                for row in csv_reader:
                   quantile.append(row)

            #remove unneccessary values
            quantile = quantile[(len(quantile)-1)]
            #get the classes
            class_number = quantile[0].split(":")
            quantile[0] = 0.0
            quantile = [float(x) for x in quantile]
            return {"class_number":int(class_number[0]),"values":quantile}

        except:
            return False

    def createAllServices(self):
        ind_values = IndicatorValues('raster')
        wms_values = ind_values.getAllAvaliableServiceValues(self.service)
        results = []

        for x in wms_values:
            cat = x['cat_name']
            cat = cat.replace("ä","ae").replace("ö","oe").replace("ü","ue")
            values = x['values']
            #get the possible rster extends
            for val in values:
                ind_id = val["id"]
                ind_name = val['ind_name']
                ind_description = val['interpretation'].replace('"', "'").replace("\n", "")
                times = val["times"]
                methodology = self.toolbox.clean_string(val["methodik"])
                unit = val["unit"]
                colors=val["colors"]
                url_spatial_extend = '%s?values={"ind":{"id":"%s"},"format":{"id":"raster"},"query":"getSpatialExtend"}' % (Config.URL_BACKEND_SORA, ind_id)
                extends_request = requests.get(url_spatial_extend)
                extends = json.loads(extends_request.text)
                # builder
                try:
                     self.indicator=Indicator(ind_id,ind_name,ind_description,times,extends,unit,methodology,colors,cat)
                     results.append(self.writeFile())
                except IOError as e:
                    app.logger.debug("Error in create WMS_service for Indicator:\n {}\n{}\n{}\n{}".format(ind_id,times,extends,e))
                    #print("Error in create WMS_service for Indicator:\n {}\n{}\n{}\n{}".format(ind_id,times,extends,e))

        return results

    def createSingleService(self, Indicator,file_path=None):
        self.indicator = Indicator
        return(self.writeFile(file_path))
    '''
    old version creates mapfiles for the old mapserver
    '''

    def writeFile(self, file_path=None,old_version=False):
        try:
            # extract the times
            time_array = self.indicator.get_time().split(",")

            # get quantile
            app.logger.debug("Indicator:\n {0}".format(self.indicator.toJSON()))
            classes = self.getQuantil(self.indicator.get_id(),self.indicator.get_spatial_extends()[0],time_array[0])["class_number"]
            colors = Color(self.indicator.get_colors()["min"],self.indicator.get_colors()["max"],classes)
            colorPalette= colors.buildColorPalette()
            os.chdir(self.path)

            if old_version:
                file = codecs.open('{}_{}_100.map'.format(self.indicator.get_cat(), self.indicator.get_id().upper()), 'w',
                               "utf-8")
            else:
                file = codecs.open('wms_{}.map'.format(self.indicator.get_id().lower()), 'w', "utf-8")

            header = ("MAP\n"
                        'NAME "WMS {0}"\n'
                        "STATUS ON\n"
                        "EXTENT 4000000 2650000 4700000 3600000\n"
                        "UNITS METERS\n"
                        'SHAPEPATH "../data"\n'
                        'FONTSET "../mapfiles/fonts/fonts.txt"\n'
                        "IMAGECOLOR 255 255 255\n"
                        'CONFIG "MS_ERRORFILE" "/mapsrv_daten/detailviewer/log/ms_log.txt"\n'
                        'CONFIG "PROJ_LIB" "/usr/share/proj/"\n\n'.format(self.indicator.get_name()))

            file.write(header)

            meta = ("WEB\n"
                    'IMAGEPATH "/srv/www/htdocs/ms_tmp/"\n'
                    'IMAGEURL "/ms_tmp/"\n'
                                       '    METADATA\n'
                       '        "wcs_title"  "wms {0}"\n'
                       '        "wms_abstract" "{1}"\n'
                       '        "wms_label" "{0}"\n'
                       '        "wms_description" "{2}"\n'
                       '        "wms_fees" "none"\n'
                       '        "wms_accessconstraints" "none"\n'
                       '        "wms_keywordlist" "wms,{0}"\n'
                       '        "wms_address" "Weberplatz 1"\n'
                       '        "wms_city" "Dresden"\n'
                       '        "wms_stateorprovince" "Sachsen"\n'
                       '        "wms_postcode" "01217"\n'
                       '        "wms_country" "Deutschland"\n'
                       '        "wms_contactelectronicmailaddress" "monitor@ioer.de"\n'
                       '        "wms_contactperson" "Dr.-Ing. Gotthard Meinel"\n'
                       '        "wms_contactorganization" "Leibniz Institut für ökologische Raumentwicklung"\n'
                       '        "wms_contactposition" "Forschungsbereichsleiter"\n'
                       '        "wms_contactvoicetelephone" "0351/4679254"\n'
                       '        "wms_feature_info_mime_type" "text/html" \n'
                       '        "wms_enable_request" "*"\n'
                       '        "wms_encoding" "UTF-8"\n'
                       '    END\n'
                       'END\n\n'
                       'PROJECTION\n'
                       '    "init=epsg:3035"\n'
                       'END\n\n'.format(self.indicator.get_name(),self.indicator.get_methodogy(),self.indicator.get_description()))

            file.write(meta)

            legend = ("LEGEND\n"
                      "     STATUS ON\n"
                      "     KEYSIZE 18 12\n"
                      "     LABEL\n"
                      "     TYPE BITMAP\n"
                      "     SIZE MEDIUM\n"
                      "     COLOR 0 0 89\n"
                      "     END\n"
                      '     TEMPLATE "/mapsrv_daten/detailviewer/mapfiles/legend.html"\n'
                      "END\n\n")

            file.write(legend)

            for t in sorted(time_array):
                int_time = int(t)
                now = datetime.datetime.now()
                if int_time >= 2006 and int_time <= now.year:
                    for s in self.indicator.get_spatial_extends():
                        layer=("LAYER\n"
                                '   NAME "{0}_{1}_{2}m"\n'
                                "   METADATA\n"
                                '       "wms_title" "{0}_{1}_{2}m"\n'
                                '       "wms_extent" "4000000 2650000 4700000 3600000"\n'
                                '       "wms_srs" "epsg:25832 epsg:25833 epsg:31466 epsg:31467 epsg:31468 epsg:31469 epsg:3034 epsg:3035 epsg:3044 epsg:3857 epsg:4258 epsg:4326"\n'
                                '       "wms_feature_info_mime_type" "text/html" \n'
                                '   END\n'
                               '    TYPE RASTER\n'
                               '    STATUS ON\n'
                                '   PROJECTION\n'
                                '       "init=epsg:3035"\n'
                                '   END\n'
                                '   PROCESSING "SCALE=-1,101"\n'
                                '   PROCESSING "RESAMPLE=NEAREST"\n'
                                '   DATA "./{1}/Raster {2} m/r{2}_{1}_{0}.tif"\n'
                                '   TEMPLATE "template.html"\n'
                                '   TOLERANCE 0\n'
                                '   TOLERANCEUNITS pixels\n\n'.format(self.indicator.get_id(),t,s)
                               )

                        file.write(layer)
                        try:
                            quantile = self.getQuantil(self.indicator.get_id(),s,t)["values"]
                            max = quantile[(len(quantile)-1)]
                            i=0
                            for x in quantile:
                                i +=1
                                if i<(len(quantile)-1) and x != max:
                                    min = x
                                    after = quantile[i]
                                    color=colorPalette[i]
                                elif x==max:
                                    min = quantile[(len(quantile) - 2)]
                                    after = max
                                    color = colorPalette[classes]

                                wms_class=('    CLASS \n'
                                           '        NAME "> {0} bis {1} "\n'
                                           '        EXPRESSION ([pixel] >  {0} and [pixel] <=  {1})\n'
                                           '        STYLE\n'
                                           '        COLOR "{2}"\n'
                                           '        END\n'
                                           '    END\n'.format(min,after,color))

                                file.write(wms_class)
                        except:
                            print("no quantil are avaliable for {}_{}_{}".format(self.indicator.get_id(),s,t))

                        file.write("END\n\n")

            created_layer = self.indicator.toJSON()
            app.logger.debug("Finished WMS_service for Indicator:\n {0}".format(created_layer))
            file.write("END")
        except IOError as e:
            created_layer = self.indicator.toJSON("I/O error({0})".format(e))
            app.logger.debug("Error in create WMS_service for Indicator:\n {0}".format(created_layer))

        return created_layer
