# -*- coding: utf-8 -*-
from flask import render_template, jsonify
from app.admin import admin
from app.admin.services.Wfs import Wfs
from app.admin.services.Wcs import Wcs

@admin.route('/')
def admin_page():
    return render_template("admin/index.html")

@admin.route('/wfs',methods=['GET', 'POST'])
def wfs_service():
    wfs = Wfs()
    return jsonify(wfs.createAllServices())

@admin.route('/wcs',methods=['GET', 'POST'])
def wcs_service():
    wcs = Wcs()
    return jsonify(wcs.createAllServices())

