from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('Benutzername', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Passwort', validators=[InputRequired()])
    remember_me = BooleanField('An mich erinnern')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='keine gültige Mailadresse')])
    username = StringField('Benutzername', validators=[InputRequired()])
    password = PasswordField('Kennwort', validators=[InputRequired(),validators.EqualTo('repeat_password', message='Passwörter müssen übereinstimmen')])
    repeat_password = PasswordField('Kennwort wiederholen')
    lastname = StringField('Familienname', validators=[InputRequired()])
    firstname = StringField('Vorname', validators=[InputRequired()])
    facility = StringField('Einrichtung')
    business_list = ('Bitte Wählen','Bundesverwaltung', 'Landesverwaltung', 'Kreis-/Kommunalverwaltung', 'Privatwirtschaft', 'Wissenschaft', 'Bildung', 'NGO', 'Privatperson', 'sonstiges')
    business = SelectField(label='Branche',choices=[(state, state) for state in business_list],validators=[InputRequired()])
    conditions = BooleanField("Ich stimme der Benutzungsordnung zu. Ich stimme zu, dass meine persönlichen Daten vom IÖR zur Erbringung dieser Dienstleistung genutzt werden. Dies schließt auch die Information von Primärforschern oder Datengebern über die Datennutzung ein. Weitere Informationen zum Datenschutz finden sich im <a target='_blank' href='https://www.ioer.de/impressum/'>IÖR-Monitor Impressum</a>.", default=False,validators=[InputRequired()])

class ResetPasswordMailForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='keine gültige Mailadresse')])

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Kennwort', validators=[InputRequired(), validators.EqualTo('repeat_password',
                                                                                         message='Passwörter müssen übereinstimmen')])
    repeat_password = PasswordField('Kennwort wiederholen')