# -*- coding: utf-8 -*-
from flask import render_template,request,Markup,jsonify,redirect,session
from flask_login import login_user, LoginManager, current_user, login_required, logout_user
from flask import url_for
from flask import Response

from app.ogc.models.forms import *
from app.ogc.models.users import * 
from werkzeug.security import check_password_hash, generate_password_hash

from app.ogc import ogc
from app import app,db

import requests

login_manager = LoginManager()
login_manager.init_app(app)

@ogc.route('/')
def index():
    return render_template('user/index.html')

@login_manager.user_loader
def load_user(user_id):
    return USER.query.get(int(user_id))

@ogc.route('/ogc', methods=['GET', 'POST'])
def get_service():
    #get all url parameter
    url = request.url.split("?")
    parameters = url[1].split("&")
    service = ''
    id=''
    key = ''
    paramater_ogc = ''
    for x in parameters:
        x_str = x.lower()
        if 'key' in x:
            key = x.replace('key=','')
        elif 'service' in x_str:
            service = x_str.replace('service=','')
        elif 'id' in x_str:
            id=x_str.replace('id=','')
        else:
            paramater_ogc +='&'+x_str
    url_ogc ="https://monitor.ioer.de/cgi-bin/mapserv?map=/mapsrv_daten/detailviewer/{}_mapfiles/{}_{}.map&SERVICE={}{}".format(service.lower(),service.lower(),id.upper(),service.upper(),paramater_ogc)
    req = requests.get(url_ogc, stream=True)
    response = Response(req.text,status = req.status_code,content_type = req.headers['content-type'])
    if session.get('key') is not None:
         return response
    else:
        cur_key = db.engine.execute("SELECT * FROM users WHERE api_key='{}'".format(key))
        if cur_key.rowcount == 0:
            return jsonify({"error":"Wrong API Key"})
        else:
            session['key'] = True
            return response

@ogc.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.access == 2:
            # ToDo redirect is not working-> somewhere is a mistake
            return redirect("https://{}/monitor_api/admin".format(request.host))
        else:
            return render_template('user/api_key.html', key=current_user.api_key, btn_text='Kopieren',
                                   username=current_user.username,
                                   user_id=current_user.id)
    form = LoginForm()
    if form.validate_on_submit():
        user = USER.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            if current_user.access == 2:
                return redirect("https://{}/monitor_api/admin".format(request.host))
            else:
                return render_template('user/api_key.html', key=current_user.api_key, btn_text='Kopieren', username=current_user.username,
                                       user_id=current_user.id)
        else:
            error = Markup('Der <b>Nutzername</b> oder <b>Passwort</b> falsch')
            return render_template('user/login.html', form=form, error=error)

    return render_template('user/login.html', form=form)

@ogc.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(form_type="inline")
    if form.validate_on_submit():
        #Form Values
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        username = form.username.data
        email = form.email.data
        cur_user = db.engine.execute("SELECT * FROM users WHERE username='{}'".format(username))
        cur_mail = db.engine.execute("SELECT * FROM users WHERE email='{}'".format(email))
        if cur_user.rowcount > 0:
            error = Markup('Der <b>Nutzername</b> existiert bereits, bitte wählen Sie einen andere')
            return render_template('user/signup.html', form=form, error=error)
        elif cur_mail.rowcount > 0:
            error = Markup('Die <b>Email-Adresse</b> existiert bereits, bitte wählen Sie eine andere')
            return render_template('user/signup.html', form=form, error=error)
        else:
            new_user = USER(username=username, email=email, password=hashed_password, lastname=form.lastname.data, firstname=form.firstname.data, facility=form.facility.data,access=1)
            db.session.add(new_user)
            db.session.commit()
            login_user(USER.query.filter_by(username=username).first())
            return render_template('user/api_key.html', key='', btn_text='Generieren', username=current_user.username, user_id=current_user.id, access=1)
    return render_template('user/signup.html', form=form)

@ogc.route('/services',methods=['GET','POST'])
def user_services():
    if current_user.is_authenticated:
        return render_template('user/services.html', key=current_user.api_key, access=current_user.access)
    else:
       return redirect("https://{}/monitor_api/login".format(request.host))

@ogc.route('/api_key')
def api_key():
    if current_user.is_authenticated:
        key = current_user.api_key
        return render_template('user/api_key.html', key=key, username=current_user.username, user_id=current_user.id, access=current_user.access)
    else:
        return url_for('ogc.login')

@ogc.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("https://{}/monitor_api".format(request.host))

@ogc.route('/check_key',methods=['GET', 'POST'])
def check_key():
    key=request.args.get('key')
    cur_key = db.engine.execute("SELECT api_key FROM users WHERE api_key='{}'".format(key))
    if cur_key.rowcount >0:
        return jsonify(True)
    else:
        return  jsonify(False)

@ogc.route('/insert_key',methods=['GET', 'POST'])
def insert_key():
    key=request.args.get('key')
    name=request.args.get('name')
    id=request.args.get('id')
    try:
        db.engine.execute("UPDATE users set api_key='{}' where username='{}' and id={}".format(key,name,id))
        return jsonify(True)
    except:
        return jsonify(False)
