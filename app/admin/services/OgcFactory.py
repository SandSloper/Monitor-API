from flask import request

from app.admin.services.WcsService import WcsService
from app.admin.services.WfsService import WfsService
from app.admin.services.WmsService import WmsService

from app import *

class OgcFactory:
    def __init__(self,_service):
        self.service = _service.lower()
        if("localhost" in request.url or "127.0.0.1:5000" in request.url):
            app.logger.debug("OGC Service for localhost")
            self.path ='G:\\mapsrv_daten\\detailviewer\\{}_mapfiles'.format(self.service)
        else:
            app.logger.debug("OGC Service for monitor.ioer.de")
            self.path = '/mapsrv_daten/detailviewer/{}_mapfiles'.format(self.service)

    def create_service(self):
        if self.service =='wms':
            return WmsService(self.path)
        elif self.service =='wcs':
            return WcsService(self.path)
        elif self.service=='wfs':
            return WfsService(self.path)