from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL
from news_app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if(user):
            raise ValidationError('Username is taken')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if(email):
            raise ValidationError('Email is taken')


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField(label='Log in')


class CompanyForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(), Length(min=3, max=30)])
    base_url = StringField(label='URL', validators=[DataRequired(), Length(min=5, max=50), URL()])
    html_element = StringField(label='HTML Element', validators=[DataRequired(), Length(min=1, max=20)])
    element_class = StringField(label='Element Class', validators=[Length(min=1, max=50)])
    html_label = StringField(label='HTML label', validators=[Length(min=1, max=20)])
    label_class = StringField(label='Label Class', validators=[Length(min=1, max=50)])
    submit = SubmitField(label='Add')


class RequestResetForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label='Add')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if(user is None):
            raise ValidationError('There is no account with this email. Please register to continue.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Reset')