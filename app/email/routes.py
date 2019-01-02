from flask import request, jsonify
from flask_mail import Mail, Message

from app import app

from app.email import mail

@mail.route('/', methods=['GET', 'POST'])
def send():
    sender = request.args.get('sender')
    message = request.args.get('message')
    name = request.args.get('name')

    mail = Mail(app)
    msg = Message(body=message,
                  sender=sender,
                  subject='IÖR-Feedback from: {}'.format(name),
                  recipients=["l.mucha@ioer.de","monitor@ioer.de"])
    app.logger.debug("send Mail from:{} \n message:{} \n sendto:{}".format(sender,message,"l.mucha@ioer.de || monitor@ioer.de"))
    mail.send(msg)
    return jsonify("send")
