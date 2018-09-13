# -*- coding: utf-8 -*-
from flask import render_template,request,Markup,jsonify,redirect
from flask_login import login_user,LoginManager
from flask import stream_with_context
from flask import Response
from app.ogc.forms import *

from app.ogc.models import *
from werkzeug.security import check_password_hash, generate_password_hash

from app.ogc import ogc
from app import app,db

import requests

login_manager = LoginManager()
login_manager.init_app(app)

@ogc.route('/')
def index():
    return render_template('index.html')

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
    url = request.url.split("?")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("{}?{}&{}".format("https://monitor.ioer.de/monitor_test/", url[1],"log=true"))
            login_user(user, remember=form.remember_me.data)

    return render_template('login.html', form=form)

@ogc.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
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
            return "<h1>Logged in</h1>"
    return render_template('signup.html', form=form)
