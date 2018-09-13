from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('Benutzername', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Passwort', validators=[InputRequired()])
    remember_me = BooleanField('An mich erinnern')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='keine gültige Mailadresse'), Length(max=50)])
    username = StringField('Benutzername', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Kennwort', validators=[InputRequired(),validators.EqualTo('repeat_password', message='Passwörter müssen übereinstimmen')])
    repeat_password = PasswordField('Kennwort wiederholen')
    lastname = StringField('Familienname', validators=[InputRequired(), Length(min=4, max=15)])
    firstname = StringField('Vorname', validators=[InputRequired(), Length(min=4, max=15)])
    facility = StringField('Einrichtung', validators=[InputRequired()])
    conditions = BooleanField("Ich stimme der Benutzungsordnung zu. Ich stimme zu, dass meine persönlichen Daten vom IÖR zur Erbringung dieser Dienstleistung genutzt werden. Dies schließt auch die Information von Primärforschern oder Datengebern über die Datennutzung ein. Weitere Informationen zum Datenschutz finden sich im IÖR-Monitor Impressum unten.", default=False,validators=[InputRequired()])
