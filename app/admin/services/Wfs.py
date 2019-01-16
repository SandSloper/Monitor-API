# -*- coding: utf-8 -*-
import os
import codecs
from app.admin.services.IndicatorValues import IndicatorValues
from app.tools.Toolbox import Toolbox
import datetime

class Wfs:
    def __init__(self):
        self.service='wfs'
        #server
        #self.path=os.chdir('/mapsrv_daten/detailviewer/wfs_mapfiles')
        self.path = os.chdir('G:\\mapsrv_daten\\detailviewer\\wfs_mapfiles')
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
                results.append(self.writeFile(id=ind_id, name=ind_name, description=ind_description, time_string=times, spatial_extends=spatial_extends, units=unit, methodology=methodology))
        return results

    def createSingleService(self,id, name, description, time_string, spatial_extends, units, methodology):
        self.writeFile(id,name,description,time_string,spatial_extends,units,methodology)

    def writeFile(self, id, name, description, time_string, spatial_extends, units, methodology):
        try:
            # extract the times
            time_array = time_string.split(",")

            file = codecs.open('wfs_{}.map'.format(id.upper()), 'w',"utf-8")

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
                        'IMAGEURL "/ms_tmp/"\n'.format(name))

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
                "END \n"
            "END \n".format(name,description,methodology))

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
                now = datetime.datetime.now()
                if int_time>2006 and int_time<=now.year:
                    for s in spatial_extends:
                        int_s = int(spatial_extends[s])
                        if int_s==1:
                            epsg = '25832'
                            geometry = 'the_geom'
                            # geometry column is different for timeshifts in the year 2000

                            if s != 'g50' or s != 'sst':
                                if int_time <= 2012:
                                    epsg = '31467'

                            sql = '{0} from (select g.gid, g.ags, g.{0}, g.gen, a."{1}" as value from vg250_{2}_{3}_grob g join basiskennzahlen_{3} a on g.ags = a.ags where a."{1}" >=-1) as subquery using unique gid using srid={4}'.format(geometry,id,s,t,epsg)

                            layer = ('LAYER \n'
                                    '  NAME "{0}_{1}" \n'
                                    '  METADATA \n'
                                    '       "wfs_title" "{2} {1}" \n'
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
                                    '\n'.format(s,t,name,description,epsg,units,sql))

                            file.write(layer)
            created_layer = {id: {
                "state":"created",
                "name": name,
                "description": description,
                "times":time_string,
                "spatial_extends":spatial_extends,
                "unit":units,
                "methodik":methodology
            }}
            file.write("END")
        except IOError as e:
            created_layer = {id: {
                "state":"I/O error({0})".format(e),
                "name": name,
                "description": description,
                "times": time_string,
                "spatial_extends": spatial_extends,
                "unit": units,
                "methodik": methodology
            }}

        return created_layer



