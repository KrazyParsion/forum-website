from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired, Length, EqualTo 

class RegistrationForm(FlaskForm): 
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) 
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm): 
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Sign In')

class PostForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    content = StringField(validators=[DataRequired()])
    post = SubmitField('Post')

class CommentForm(FlaskForm):
    content = StringField(validators=[DataRequired()])
    submit = SubmitField("Comment")
