from flask_mail import Mail, Message
from app import app

class Mailer:

    def __init__(self,to,subject,template):
        self.to = to
        self.subject=subject
        self.template = template

    def send_email(self):
        mail = Mail(app)
        print(self.subject,self.to,self.template)
        msg = Message(
            subject=self.subject,
            recipients=[self.to],
            html=self.template,
            sender='monitor@ioer.de'
        )
        mail.send(msg)