# -*- coding: utf-8 -*-
import requests
from flask import jsonify,request
from flask_mail import Mail, Message
from app.monitor import monitor
from app.admin.models.IndicatorValues import IndicatorValues
from app.config import Config
from app import app

'''
Mails
'''
@monitor.route('/mail', methods=['GET', 'POST'])
def send():
    sender = request.args.get('sender')
    message = request.args.get('message')
    name = request.args.get('name')

    mail = Mail(app)
    msg = Message(body=message,
                  sender=sender,
                  subject='IÖR-Feedback from: {}'.format(name),
                  recipients=["monitor@ioer.de"])
    app.logger.debug("send Mail from:{} \n message:{} \n sendto:{}".format(sender,message,"monitor@ioer.de"))
    mail.send(msg)
    return jsonify("send")
@monitor.route('/error_mail', methods=['GET', 'POST'])
def send_error():
    message = request.args.get('message')
    name = request.args.get('name')

    mail = Mail(app)
    msg = Message(body=message,
                  subject='ERROR im Monitor bei: {}'.format(name),
                  sender="ERROR Monitor",
                  recipients=["l.mucha@ioer.de"])
    app.logger.debug("send Mail for Error: \n message:{} \n sendto:{}".format(message,"l.mucha@ioer.de"))
    mail.send(msg)
    return jsonify("send")
'''
Method which create the cache, requesting all possebilies and insert them in the PostgreSQL DB
'''
@monitor.route('/cache',methods=['GET'])
def set_cache():
    # first clear cache
    created = []
    req = requests.post(Config.URL_BACKEND_MONITOR_ADMIN, data={'values': '{"query":"clearcache"}'})
    if "done" in req.text:
        values = IndicatorValues("gebiete")
        res = values.getAllAvaliableServiceValues("wfs")
        for i in res:
            for val in i["values"]:
                id = val["id"]
                times = val["times"].split(",")
                spatial_extends = val["spatial_extends"]
                # request for each time and each spatial unit
                for t in times:
                    for sp in spatial_extends:
                        if int(spatial_extends[sp])==1:
                            json = '{"ind":{"id":"'+id+'","time":"'+t+'","raumgliederung":"'+sp+'","klassifizierung":"haeufigkeit","klassenzahl":"7"},"format":{"id":"gebiete"},"query":"getJSON"}'
                            print(json)
                            created.append(json)
                            requests.post(Config.URL_BACKEND_MONITOR,data={'values':json})
        return jsonify(created)
    else:
        return jsonify("error")

