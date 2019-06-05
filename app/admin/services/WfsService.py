# -*- coding: utf-8 -*-
import os
import codecs

from app import *
from app.admin.services.IndicatorValues import IndicatorValues
from app.admin.models.Toolbox import Toolbox
from app.admin.models.IoerIndicator import IoerIndicator
from app.admin.interfaces.OgcService import OgcService

class WfsService(OgcService):
    indicator = None
    def __init__(self,path='/mapsrv_daten/detailviewer/wfs_mapfiles'):
        self.service='wfs'
        self.path=os.chdir(path)
        self.toolbox = Toolbox()

    def createAllServices(self):
        ind_values = IndicatorValues('gebiete')
        wfs_values = ind_values.getAllAvaliableServiceValues(self.service)
        results = []
        for x in wfs_values:
            values = x['values']
            for val in values:
                ind_id = val["id"]
                ind_name = val['ind_name']
                ind_description = val['interpretation'].replace('"',"'").replace("\n","")
                times = val["times"]
                spatial_extends = val["spatial_extends"]
                methodology = self.toolbox.clean_string(val["methodik"])
                unit = val["unit"]
                #builder
                self.indicator = IoerIndicator(ind_id, ind_name, ind_description, times, spatial_extends, unit, methodology)
                results.append(self.__writeFile())
        return results

    def createSingleService(self,Indicator,file_path=None):
        self.indicator=Indicator
        self.__writeFile(file_path)

    def __writeFile(self, file_path=None):
        try:
            # extract the times
            time_array = self.indicator.get_time().split(",")
            if file_path:
                file = codecs.open(file_path, 'w',"utf-8")
            else:
                file = codecs.open('wfs_{}.map'.format(self.indicator.get_id().upper()), 'w', "utf-8")
            '''
                The following File is created by taking care of the documentation of the Mapserver:  
                https://mapserver.org/ogc/wfs_server.html
            '''
            header = ('MAP \n'
                        'NAME "WFS {0}"\n'
                        'STATUS ON\n'
                        'EXTENT 280371.03 5235855.50 921120.19 6101444.00\n'
                        'UNITS METERS\n'
                        'SHAPEPATH" ../data"\n'
                        'CONFIG "PROJ_LIB"  "/usr/share/proj/"\n'
                        'WEB\n'
                        'IMAGEPATH "/srv/www/htdocs/ms_tmp/"\n'
                        'IMAGEURL "/ms_tmp/"\n'.format(self.indicator.get_name()))

            file.write(header)

            meta = ("WEB \n"
                '   IMAGEPATH "/srv/www/htdocs/ms_tmp/" \n'
                '   IMAGEURL "/ms_tmp/" \n'
                '   METADATA \n'
                '       "wfs_title"  "WFS {0}" \n'
                '       "wfs_abstract" "{1}" \n'
                '       "wfs_label" "WFS {0}" \n'
                '       "wfs_description"  "{2}" \n'
                '       "wfs_fees" "none" \n'
                '       "wfs_accessconstraints" "none" \n'
                '       "wfs_address" "Weberplatz 1" \n'
                '       "wfs_city" "Dresden" \n'
                '       "wfs_stateorprovince" "Sachsen" \n'
                '       "wfs_postcode" "01217" \n'
                '       "wfs_country" "Deutschland" \n'
                '       "wfs_contactelectronicmailaddress" "monitor@ioer.de" \n'
                '       "wfs_contactperson" "Dr.-Ing. Gotthard Meinel" \n'
                '       "wfs_contactorganization" "Leibniz Institut für Ökologische Raumentwicklung" \n'
                '       "wfs_contactposition" "Forschungsbereichsleiter" \n'
                '       "wfs_contactvoicetelephone" "0351/4679254" \n'
                '       "ows_role" "Erzeuger" \n'
                '       "wfs_enable_request" "*" \n'
                '       "wfs_encoding" "UTF-8" \n'
                '       "ows_enable_request" "*"\n'
                "END \n"
            "END \n".format(self.indicator.get_name(),self.indicator.get_description(),self.indicator.get_methodogy()))

            file.write(meta)

            projection = ("PROJECTION \n"
                        '   "init=epsg:25832" \n'
                        "END \n")

            file.write(projection)

            '''
            Create the single layer
            '''

            for t in sorted(time_array):
                int_time = int(t)
                if int_time>2006:
                    for s in self.indicator.get_spatial_extends():
                        int_s = int(self.indicator.get_spatial_extends()[s])
                        if int_s==1:
                            epsg = '25832'
                            geometry = 'the_geom'
                            # geometry column is different for timeshifts in the year 2000

                            if s != 'g50' or s != 'stt':
                                if int_time <= 2012:
                                    epsg = '31467'

                            sql = '{0} from (select g.gid, g.ags, g.{0}, g.gen, a."{1}" as value from vg250_{2}_{3}_grob g join basiskennzahlen_{3} a on g.ags = a."AGS" where a."{1}" >=-1) as subquery using unique gid using srid={4}'.format(geometry,self.indicator.get_id(),s,t,epsg)

                            layer = ('LAYER \n'
                                    '  NAME "{0}_{1}" \n'
                                    '  METADATA \n'
                                    '       "wfs_title" "{2} {1} an {0}" \n'
                                    '       "wfs_abstract" "{2} {1} an {0}" \n'
                                    '       "wfs_description " "{3}" \n'
                                    '       "wfs_srs" "epsg:{4}" \n'
                                    '       "gml_include_items" "all" \n'
                                    '       "wfs_enable_request" "*" \n'
                                    '       "gml_constants" "value-einheit,Indikatorname" \n'
                                    '       "gml_value-einheit_type" "string" \n'
                                    '       "gml_value-einheit_value" "{5}" \n'
                                    '       "gml_exclude_items" "gid" \n'
                                    '       "gml_Indikatorname_type" "string" \n'
                                    '       "gml_Indikatorname_value" "{2} {1}" \n'
                                    '       "gml_featureid"     "id" \n'
                                    '   END \n'
                                    '\n'
                                    '   TYPE POLYGON \n'
                                    '   STATUS ON \n'
                                    '   CONNECTIONTYPE POSTGIS \n'
                                    '   CONNECTION "host=localhost port=5432 dbname=monitor_geodat user=monitor_svg_admin password=monitorsvgadmin" \n'
                                    "   DATA '{6}' \n"
                                    ' \n'
                                    '   PROJECTION \n'
                                    '       "init=epsg:{4}" \n'
                                    '   END \n'
                                    'END \n'
                                    '\n'.format(s,t,self.indicator.get_name(),self.indicator.get_description(),epsg,self.indicator.get_units(),sql))

                            file.write(layer)
            created_layer = self.indicator.toJSON()
            app.logger.debug("Finished WMS_service for Indicator:\n {0}".format(created_layer))
            file.write("END")
        except IOError as e:
            created_layer =self.indicator.toJSON("I/O error({0})".format(e))
            app.logger.debug("Error in create WMS_service for Indicator:\n {0}".format(created_layer))
        return created_layer



