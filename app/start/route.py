from flask import Blueprint,render_template,Flask
from app.start import start

from app import app

@start.route('/')
def index():
    return render_template('index.html')
