# -*- coding: utf-8 -*-
from flask import render_template, jsonify
from flask_login import LoginManager, login_required

from app import app
from app.admin import admin
from app.admin.services.GeoSN import GeoSN
from app.admin.services.OgcFactory import OgcFactory
from app.user.models.Forms import *
from app.user.models.User import *

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    form = RegisterForm(form_type="inline")
    return render_template('user/signup.html', form=form)

@admin.route('/')
@login_required
def admin_page():
    return render_template("admin/index.html")

@admin.route('/wfs',methods=['GET', 'POST'])
@login_required
def wfs_service():
    wfs = OgcFactory('wfs')
    return jsonify(wfs.create_service().createAllServices())

@admin.route('/wcs',methods=['POST'])
@login_required
def wcs_service():
    wcs = OgcFactory("wcs")
    return jsonify(wcs.create_service().createAllServices())

@admin.route('/wms',methods=['POST'])
@login_required
def wms_service():
    wms = OgcFactory("wms")
    return jsonify(wms.create_service().createAllServices())

@admin.route('/geosn',methods=['POST'])
@login_required
def geosn_service():
    geosn = GeoSN('/srv/www/htdocs/monitor_ogc_xml/')
    return jsonify(geosn.update())
