from flask import render_template,request,Markup,jsonify,redirect
from flask_login import login_user,current_user,LoginManager
from app.users.forms import *
from app.users.models import *
from werkzeug.security import check_password_hash, generate_password_hash

from app.users import users
from app import app,db

login_manager = LoginManager()
login_manager.init_app(app)

@users.route('/login', methods=['GET', 'POST'])
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

@users.route('/signup', methods=['GET', 'POST'])
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
