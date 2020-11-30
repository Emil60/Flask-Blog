from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
class RegisterForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired(), Length(min=2, max=50)])
    email=StringField('Email',validators=[DataRequired(), Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Sign Up')

class LoginForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired(), Length(min=2, max=50)])
    
    password=PasswordField('Password',validators=[DataRequired(), Length(min=2, max=50)])
    submit=SubmitField('Sign In')

class PostForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    subtitle=StringField('Subtitle',validators=[DataRequired()])
    post_text = TextAreaField('Post text',validators=[DataRequired()])
    submit=SubmitField('Share Post')

class ContactForm(FlaskForm):
    name=StringField('Full Name',validators=[DataRequired(), Length(min=2, max=50)])
    number=StringField('Number',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(), Email()])
    message = TextAreaField('Message',validators=[DataRequired()])
    submit=SubmitField('Send Message')