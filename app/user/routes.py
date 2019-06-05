# -*- coding: utf-8 -*-
from flask_mail import Mail, Message
import requests
import datetime
from flask import render_template,request,Markup,jsonify,redirect,session,flash
from flask_login import login_user, LoginManager, current_user, login_required, logout_user
from flask import url_for
from flask import Response

from app.user.models.Forms import *
from app.user.models.User import *
from app.config import Config
from werkzeug.security import check_password_hash, generate_password_hash
from app.user.models.Token import Token
from app.user.models.Mailer import Mailer

from app.user import user
from app import app,db
# create the log in manager to handle user sessions
login_manager = LoginManager()
login_manager.init_app(app)
# token creator
token = Token()

@user.route('/')
def index():
    return render_template('user/index.html',host=Config.URL_ENDPOINT)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    form = RegisterForm(form_type="inline")
    return render_template('user/signup.html', form=form)
'''
handels the streaming of the given OGC-Service
'''
@user.route('/user', methods=['GET', 'POST'])
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
    app.logger.info("Mapserver request: %s", url_ogc)
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
'''
User Log In
'''
@user.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    if current_user.is_authenticated:
        if current_user.access == 2:
            return redirect("{}admin/".format(Config.URL_ENDPOINT))
        else:
            return render_template('user/api_key.html', key=current_user.api_key, btn_text='Kopieren',
                                   username=current_user.username,
                                   user_id=current_user.id,host=Config.URL_ENDPOINT)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            if current_user.access == 2:
                return redirect("{}admin/".format(Config.URL_ENDPOINT))
            else:
                app.logger.info("%s is logged in as user",current_user.username)
                return render_template('user/api_key.html', key=current_user.api_key, btn_text='Kopieren', username=current_user.username,
                                       user_id=current_user.id,host=Config.URL_ENDPOINT)
        else:
            error = Markup('<div class="alert alert-danger w-100" role="alert">Der <b>Nutzername</b> oder das <b>Passwort</b> ist falsch</div>')
            return render_template('user/login.html', form=form, error=error)

    return render_template('user/login.html', form=form)
'''
Registration
'''
@user.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(form_type="inline")
    if form.validate_on_submit():
        #Form Values
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        username = form.username.data
        email = form.email.data
        cur_check = db.engine.execute("SELECT email, username FROM users WHERE username='{}' or email='{}'".format(username,email)).first()
        if cur_check is not None:
            error = Markup(
                '<div class="alert alert-danger w-100" role="alert">Der <b>Nutzername</b> oder die <b>Mailadresse</b> ist schon registriert</div>')
            return render_template('user/signup.html', form=form, error=error)
        else:
            new_user = User(username=username, email=email, password=hashed_password, lastname=form.lastname.data,
                            firstname=form.firstname.data, facility=form.facility.data, access=1,
                            business=form.business.data, confirmed=False)
            db.session.add(new_user)
            db.session.commit()

            token_user = token.generate_confirmation_token(username)
            confirm_url = "{}confirm/{}".format(Config.URL_ENDPOINT, token_user)
            html = render_template('user/activate_mail.html', confirm_url=confirm_url)
            subject = "Bitte bestätigen Sie ihre Email"
            mail = Mailer(email, subject, html)
            mail.send_email()
            login_user(User.query.filter_by(username=username).first())
            return render_template('user/signup.html')
    return render_template('user/signup.html', form=form)
'''
Email confirmation
'''
@user.route('/confirm/<token_pass>')
@login_required
def confirm_email(token_pass):
    username = token.confirm_token(token_pass)
    user = User.query.filter_by(username=username).first_or_404()
    app.logger.debug("State User{0}".format(user.confirmed))
    if user.confirmed is False:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        logout_user()
        return render_template('user/confirmed_mail.html',confimed=True)
    else:
        return render_template('user/confirmed_mail.html', confimed=False)

'''
password reset
'''
@user.route('/reset',methods=['GET', 'POST'])
def send_reset_password():
    form = ResetPasswordMailForm(form_type="inline")
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user is None:
            error = Markup('<div class="alert alert-danger w-100" role="alert">Der <b>Emailadresse</b> ist nicht registriert</div>')
            return render_template('user/reset_password.html', form_mail=form,error=error)
        else:
            token_user = token.generate_confirmation_token(user.email)
            confirm_url = "{}reset/{}".format(Config.URL_ENDPOINT, token_user)
            html = render_template('user/reset_password_mail.html', confirm_url=confirm_url)
            subject = "Passwort zurücksetzen für den IÖR-Monitor"
            mail = Mailer(email, subject, html)
            mail.send_email()
            return render_template('user/reset_password.html', confimed=True)

    return render_template('user/reset_password.html',form_mail=form)

@user.route('/reset/<token_pass>',methods=['GET', 'POST'])
def reset_password(token_pass):
    form = ResetPasswordForm(form_type="inline")
    if token.confirm_token(token_pass):
        if form.validate_on_submit():
            email = token.confirm_token(token_pass)
            user = User.query.filter_by(email=email).first_or_404()
            new_pw =  generate_password_hash(form.password.data, method='sha256')
            user.password = new_pw
            db.session.add(user)
            db.session.commit()
            logout_user()
            return render_template('user/reset_password.html',reseted=True)
        return render_template('user/reset_password.html', reset_form=form)
    else:
        error = Markup('<div class="alert alert-danger w-100" role="alert">Der Token für die Zurücksetzung ist abgelaufen</div>')
        return render_template('user/reset_password.html', error=error)
'''
Service overview, shown if the USER is authenticated
'''
@user.route('/services',methods=['GET','POST'])
@login_required
def user_services():
    if current_user.is_authenticated:
        return render_template('user/services.html', key=current_user.api_key, access=current_user.access)
    else:
       return redirect("{}login".format(Config.URL_ENDPOINT))
'''
show/generate API Key
'''
@user.route('/api_key')
@login_required
def api_key():
    if current_user.is_authenticated:
        key = current_user.api_key
        return render_template('user/api_key.html', key=key, username=current_user.username, user_id=current_user.id, access=current_user.access,host=Config.URL_ENDPOINT)
    else:
        return url_for('user.login')

'''
Methods for AJAX
'''
@user.route('/check_key',methods=['GET', 'POST'])
def check_key():
    key=request.args.get('key')
    cur_key = db.engine.execute("SELECT api_key FROM users WHERE api_key='{}'".format(key))
    if cur_key.rowcount >0:
        return jsonify(True)
    else:
        return  jsonify(False)

@user.route('/insert_key',methods=['GET', 'POST'])
def insert_key():
    key=request.args.get('key')
    name=request.args.get('name')
    id=request.args.get('id')
    try:
        db.engine.execute("UPDATE users set api_key='{}' where username='{}' and id={}".format(key,name,id))
        return jsonify(True)
    except:
        return jsonify(False)

@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(Config.URL_ENDPOINT)

