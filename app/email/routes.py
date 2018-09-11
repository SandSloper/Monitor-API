from flask import request
from flask_mail import Mail, Message

from app import app

from app.email import mail

@mail.route('/', methods=['GET', 'POST'])
def send():
    sender = request.args.get('s')
    recipant = request.args.get('r')
    message= request.args.get('m')

    mail = Mail(app)
    msg = Message("Hello",
                  sender="from@example.com",
                  recipients=["l.mucha@ioer.de"])
    mail.send(msg)
    return "<h1>send</h1>"
