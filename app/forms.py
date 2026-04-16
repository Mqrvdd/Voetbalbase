from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Email


class RegisterForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Wachtwoord", validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField("Registreren")


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Wachtwoord", validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField("Inloggen")


class SpelerForm(FlaskForm):
    naam = StringField("Naam", validators=[DataRequired(), Length(max=100)])
    leeftijd = IntegerField("Leeftijd", validators=[DataRequired(), NumberRange(min=1, max=60)])
    nationaliteit = StringField("Nationaliteit", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Opslaan")


class ClubForm(FlaskForm):
    naam = StringField("Naam", validators=[DataRequired(), Length(max=100)])
    land = StringField("Land", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Opslaan")


class ContractForm(FlaskForm):
    speler_naam = StringField("Speler", validators=[DataRequired(), Length(max=100)])
    club_naam = StringField("Club", validators=[DataRequired(), Length(max=100)])
    positie = StringField("Positie", validators=[DataRequired(), Length(max=100)])
    rugnummer = IntegerField("Rugnummer", validators=[DataRequired(), NumberRange(min=1, max=99)])
    submit = SubmitField("Opslaan")