from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_ckeditor import CKEditorField


class reg_form(FlaskForm):
	name = StringField("Name:", validators=[DataRequired()])
	username = StringField("Username:", validators=[DataRequired()])
	about_author = TextAreaField("About author:")
	password = PasswordField("Password:", validators=[DataRequired(), EqualTo('password2', message="password must match")])
	profile_pic = FileField("Profile pic")
	password2 = PasswordField("Confirm Password:", validators=[DataRequired()])
	submit = SubmitField("Submit")
	
class loginform(FlaskForm):
	username = StringField("Username: ", validators=[DataRequired()])
	password = PasswordField("Password: ", validators=[DataRequired()])
	submit = SubmitField("Login")
	
class post_form(FlaskForm):
	title = StringField("Title:", validators=[DataRequired()])
	author = StringField("Author:")
	content = CKEditorField("Content:", validators=[DataRequired()])
	submit = SubmitField("Submit")
	
class SearchForm(FlaskForm):
	searched = StringField("Username: ", validators=[DataRequired()])
	submit = SubmitField("submit")