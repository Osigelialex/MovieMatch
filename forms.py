from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class profileForm(FlaskForm):
    GENRE_CHOICES = [("28", 'Action'),
                     ("12", 'Adventure'),
                     ("16", 'Animation'),
                     ("80", 'Crime'),
                     ("27", 'Horror'),
                     ('10749', 'Romance'),
                     ("99", 'Documentary'),
                     ("18", 'Drama'),
                     ("14", 'Fantasy'),
                     ("878", 'Science Fiction'),
                     ("53", 'Thriller')]


    LANGUAGE_CHOICES = ['en', 'de', 'es', 'it', 'pt', 'ko']

    genre = SelectField("Pick a preferred genre",
                        choices=GENRE_CHOICES)

    language = SelectField("Pick a preferred language",
                           choices=LANGUAGE_CHOICES)

    submit = SubmitField("Apply")
    