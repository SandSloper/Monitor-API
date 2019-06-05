# -*- coding: utf-8 -*-
import os
import codecs
import requests
import json
import datetime
from app import *
from app.config import Config
from app.admin.models.Toolbox import Toolbox
from app.admin.services.IndicatorValues import IndicatorValues
from app.admin.models.IoerIndicator import IoerIndicator
from app.admin.interfaces.OgcService import OgcService


class WcsService(OgcService):
    indicator = None

    def __init__(self, path='/mapsrv_daten/detailviewer/wcs_mapfiles'):
        self.service = 'wcs'
        self.path = os.chdir(path)
        self.toolbox = Toolbox()

    def createAllServices(self):
        ind_values = IndicatorValues('raster')
        wcs_values = ind_values.getAllAvaliableServiceValues(self.service)
        results = []
        for x in wcs_values:
            values = x['values']
            # get the possible rster extends
            for val in values:
                ind_id = val["id"]
                ind_name = val['ind_name']
                ind_description = val['interpretation'].replace('"', "'").replace("\n", "")
                times = val["times"]
                methodology = self.toolbox.clean_string(val["methodik"])
                unit = val["unit"]
                url_spatial_extend = '%s?values={"ind":{"id":"%s"},"format":{"id":"raster"},"query":"getSpatialExtend"}' % (
                Config.URL_BACKEND_SORA, ind_id)
                extends_request = requests.get(url_spatial_extend)
                extends = json.loads(extends_request.text)
                # builder
                self.indicator = IoerIndicator(ind_id, ind_name, ind_description, times, extends, unit, methodology)
                results.append(self.__writeFile())
        return results

    def createSingleService(self, indicator, file_path=None):
        self.indicator = indicator
        self.__writeFile(file_path)

    def __writeFile(self, file_path=None):
        try:
            # extract the times
            time_array = self.indicator.get_time().split(",")
            if file_path:
                file = codecs.open(file_path, 'w', "utf-8")
            else:
                file = codecs.open('wcs_{}.map'.format(self.indicator.get_id().upper()), 'w', "utf-8")

            header = ("MAP\n"
                      'NAME "WCS {0}"\n'
                      "STATUS ON \n"
                      "EXTENT 4000000 2650000 4700000 3600000\n"
                      "UNITS METERS \n"
                      'SHAPEPATH "../data" \n'
                      'FONTSET "../mapfiles/fonts/fonts.txt" \n'
                      'IMAGECOLOR 255 255 255 \n'
                      'MAXSIZE 8192\n'.format(self.indicator.get_name()))

            file.write(header)

            output_format = ("OUTPUTFORMAT\n"
                             "   NAME GTiff\n"
                             '   DRIVER "GDAL/GTiff"\n'
                             '   MIMETYPE "image/tiff"\n'
                             '   IMAGEMODE FLOAT32\n'
                             '   EXTENSION "tif"\n'
                             '   FORMATOPTION "NULLVALUE=-9998.000"\n'
                             '   FORMATOPTION "COMPRESS=LZW"\n'
                             '   FORMATOPTION "FILENAME=result.tiff"\n'
                             'END\n'
                             '\n'
                             'OUTPUTFORMAT\n'
                             '   NAME AAIGRID\n'
                             '   DRIVER "GDAL/AAIGRID"\n'
                             '   MIMETYPE "image/x-aaigrid"\n'
                             '   IMAGEMODE INT16\n'
                             '   EXTENSION "grd"\n'
                             '   FORMATOPTION "FILENAME=result.grd"\n'
                             'END\n')

            file.write(output_format)

            meta = ('CONFIG "PROJ_LIB"  "/usr/share/proj/"\n'
                    'WEB\n'
                    '    IMAGEPATH "/srv/www/htdocs/ms_tmp/"\n'
                    '    IMAGEURL "/ms_tmp/"\n'
                    '    METADATA\n'
                    '        "wcs_title"  "WCS {0}"\n'
                    '        "wcs_abstract" "{1}"\n'
                    '        "wcs_label" "{0}"\n'
                    '        "wcs_description" "{2}"\n'
                    '        "wcs_fees" "none"\n'
                    '        "wcs_accessconstraints" "none"\n'
                    '        "wcs_keywordlist" "WCS,{0}"\n'
                    '        "wcs_address" "Weberplatz 1"\n'
                    '        "wcs_city" "Dresden"\n'
                    '        "wcs_stateorprovince" "Sachsen"\n'
                    '        "wcs_postcode" "01217"\n'
                    '        "wcs_country" "Deutschland"\n'
                    '        "wcs_contactelectronicmailaddress" "monitor@ioer.de"\n'
                    '        "wcs_contactperson" "Dr.-Ing. Gotthard Meinel"\n'
                    '        "wcs_contactorganization" "Leibniz Institut für ökologische Raumentwicklung"\n'
                    '        "wcs_contactposition" "Forschungsbereichsleiter"\n'
                    '        "wcs_contactvoicetelephone" "0351/4679254"\n'
                    '        "wcs_enable_request" "*"\n'
                    '        "wcs_encoding" "UTF-8"\n'
                    '        "wcs_rangeset_nullvalue" "-9998.000"\n'
                    '        "wcs_formats" "GTiff"\n'
                    '        "wcs_nilvalues" "-9998.000"\n'
                    '        "ows_enable_request" "*"\n'
                    '    END\n'
                    'END\n'
                    'PROJECTION\n'
                    '    "init=epsg:3035"\n'
                    'END\n'.format(self.indicator.get_name(), self.indicator.get_methodogy(),
                                   self.indicator.get_description()))

            file.write(meta)

            '''
            Create the single layer
            '''

            for t in sorted(time_array):
                int_time = int(t)
                now = datetime.datetime.now()
                if int_time >= 2006 and int_time <= now.year:
                    for s in self.indicator.get_spatial_extends():
                        layer = ("Layer\n"
                                 '    NAME "{0}_{1}_{2}m"\n'
                                 '    METADATA\n'
                                 '        "wcs_label" "{0}_{1}_{2}m" \n'
                                 '        "wcs_rangeset_name" "{3}"\n'
                                 '        "wcs_description "  "{4}"\n'
                                 '        "wcs_extent" "4005000.000000 2655000.000000 4695000.000000 3595000.000000"\n'
                                 '        "wcs_cellsize" "{2}"\n'
                                 '    END\n'
                                 '    TYPE RASTER\n'
                                 '    STATUS ON\n'
                                 '    DATA "./{1}/Raster {2} m/r{2}_{1}_{0}.tif"\n'
                                 '    PROJECTION\n'
                                 '       "init=epsg:3035"\n'
                                 '    END\n'
                                 'END\n'.format(self.indicator.get_id(), t, s, self.indicator.get_name(),
                                                self.indicator.get_description())
                                 )
                        file.write(layer)

            created_layer = self.indicator.toJSON()
            app.logger.debug("Finished WMS_service for Indicator:\n {0}".format(created_layer))
            file.write("END")

        except IOError as e:
            created_layer = self.indicator.toJSON("I/O error({0})".format(e))
            app.logger.debug("Error in create WMS_service for Indicator:\n {0}".format(created_layer))
        return created_layer
