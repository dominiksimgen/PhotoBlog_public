from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, FileField
from wtforms.validators import DataRequired, URL, Optional
from flask_wtf.file import FileAllowed


class CreatePostForm(FlaskForm):
    img = FileField("Select your image",  validators=[DataRequired(),FileAllowed(['jpg', 'jpeg'],'Only "jpg" and "jpeg" files are supported!')])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    maps_url = StringField("Maps URL (Optional)", validators=[ Optional(),URL()])
    body = TextAreaField("Write a caption...", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class CreateCommentForm(FlaskForm):
    comment = TextAreaField("Write a comment...", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")

class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField("Let me in!")


class RegisterForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = StringField(label="Password", validators=[DataRequired()])
    name = StringField(label="Username", validators=[DataRequired()])
    submit = SubmitField("Sign me up!")