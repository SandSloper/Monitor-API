# -*- coding: utf-8 -*-
from flask import render_template, jsonify
from app.admin import admin
from app.admin.services.Wfs import Wfs
from app.admin.services.Wcs import Wcs
from app.admin.services.Wms import Wms

@admin.route('/')
def admin_page():
    return render_template("admin/index.html")

@admin.route('/wfs',methods=['GET', 'POST'])
def wfs_service():
    wfs = Wfs('G:\\mapsrv_daten\\detailviewer\\wfs_mapfiles')
    #wfs = Wfs()
    return jsonify(wfs.createAllServices())

@admin.route('/wcs',methods=['POST'])
def wcs_service():
    wcs = Wcs('G:\\mapsrv_daten\\detailviewer\\wcs_mapfiles')
    #wcs = Wcs()
    return jsonify(wcs.createAllServices())

@admin.route('/wms',methods=['POST'])
def wms_service():
    wms = Wms('G:\\mapsrv_daten\\detailviewer\\wms_mapfiles')
   # wms = Wms()
    return jsonify(wms.createAllServices())

