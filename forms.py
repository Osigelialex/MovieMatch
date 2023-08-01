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
    genre = SelectField("Pick a preferred genre",
                        choices=[("28", 'Action'),
                                  ("12", 'Adventure'),
                                  ("16", 'Animation'),
                                  ("35", 'Comedy'),
                                  ("80", 'Crime'),
                                  ("99", 'Documentary'),
                                  ("18", 'Drama'),
                                  ("14", 'Fantasy'),
                                  ("878", 'Science Fiction'),
                                  ("53", 'Thriller')
                                ])
    rated = SelectField("What movie rating do you prefer?",
                        choices=['G',
                                 'PG',
                                 'PG-13',
                                 'R',
                                 'NC-17'])
    language = SelectField("Pick a preferred language",
                           choices=['en',
                                    'de',
                                    'es',
                                    'it',
                                    'pt',
                                    'ko'])
    submit = SubmitField("Apply")
    