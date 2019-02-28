from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    phone_number1 = TextField('Phone #1', validators=[DataRequired()])
    phone_number2 = TextField('Phone #2', validators=[DataRequired()])
    submit = SubmitField('Sign In')