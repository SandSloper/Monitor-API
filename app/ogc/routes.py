# -*- coding: utf-8 -*-
from flask import render_template,request,Markup,jsonify,redirect
from flask_login import login_user, LoginManager, current_user, login_required, logout_user
from flask import stream_with_context, url_for, session
from flask import Response
from app.ogc.forms import *

from app.ogc.models import *
from werkzeug.security import check_password_hash, generate_password_hash

from app.ogc import ogc
from app import app,db

import requests

login_manager = LoginManager()
login_manager.init_app(app)

@ogc.route('/index')
@ogc.route('/')
def index():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    url_ogc = 'http://maps.ioer.de/cgi-bin/{}?MAP={}_{}&SERVICE={}{}'.format(service,id.upper(),service,service.upper(),paramater_ogc.upper())
    #check the key
    cur_key = db.engine.execute("SELECT * FROM users WHERE api_key='{}'".format(key))
    if cur_key.rowcount == 0:
        return jsonify({"error":"Wrong API Key"})
    else:
        req = requests.get(url_ogc, stream=True)
        return Response(stream_with_context(req.iter_content()), content_type=req.headers['content-type'])
@ogc.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('ogc.api_key'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('ogc.api_key'))
            login_user(user, remember=form.remember_me.data)

    return render_template('login.html', form=form)

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
            return render_template('signup.html', form=form, error=error)
        elif cur_mail.rowcount > 0:
            error = Markup('Die <b>Email-Adresse</b> existiert bereits, bitte wählen Sie eine andere')
            return render_template('signup.html', form=form, error=error)
        else:
            new_user = User(username=username, email=email, password=hashed_password,lastname=form.lastname.data,firstname=form.firstname.data,facility=form.facility.data)
            db.session.add(new_user)
            db.session.commit()
            return render_template('api_key.html')
    return render_template('signup.html', form=form)

@ogc.route('/api_key')
def api_key():
    key = current_user.api_key
    btn_text = "Generieren"
    key_text = ''
    if key:
        btn_text = "Kopieren"
        key_text = key

    return render_template('api_key.html',key=key_text, btn_text=btn_text,username=current_user.username,user_id=current_user.id)

@ogc.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('ogc.index'))

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