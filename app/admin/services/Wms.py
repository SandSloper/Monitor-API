# -*- coding: utf-8 -*-
import os
import codecs
import requests
import json
import datetime
from app.config import Config
from app.tools.Toolbox import Toolbox
from app.admin.services.IndicatorValues import IndicatorValues

class Wcs:
    def __init__(self):
        self.service = 'wcs'
        # server
        #self.path = os.chdir('/mapsrv_daten/detailviewer/wms_mapfiles')
        self.path = os.chdir('G:\\mapsrv_daten\\detailviewer\\wms_mapfiles')
        self.toolbox = Toolbox()