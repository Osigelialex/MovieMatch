from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class recommendationForm(FlaskForm):
    GENRE_CHOICES = [("28", 'Action'),
                     ("12", 'Adventure'),
                     ("16", 'Animation'),
                     ("35", 'Comedy'),
                     ("80", 'Crime'),
                     ("27", 'Horror'),
                     ('10749', 'Romance'),
                     ("99", 'Documentary'),
                     ("18", 'Drama'),
                     ("14", 'Fantasy'),
                     ("878", 'Science Fiction'),
                     ("53", 'Thriller')]

    RATED_CHOICES = ['G', 'PG', 'PG-13', 'R', 'NC-17']

    LANGUAGE_CHOICES = ['en', 'de', 'es', 'it', 'pt', 'ko']

    genre = SelectField("Pick a preferred genre",
                        choices=GENRE_CHOICES)

    rated = SelectField("What movie rating do you prefer?",
                        choices=RATED_CHOICES)

    language = SelectField("Pick a preferred language",
                           choices=LANGUAGE_CHOICES)

    submit = SubmitField("Apply")
    