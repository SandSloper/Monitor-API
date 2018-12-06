# -*- coding: utf-8 -*-
from flask import render_template,request,redirect
from flask_login import LoginManager, current_user

from app.ogc.models.users import * 

from app.admin import admin
from app import app

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return USER.query.get(int(user_id))


@admin.route('/')
def admin():
    if current_user.is_authenticated:
        if current_user.access == 2:
            return render_template("admin/index.html")
    else:
        return redirect("https://{}/monitor_api/login".format(request.host))
