from wtforms import Form, StringField,FileField,  validators, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_wtf import FlaskForm 
from wtforms import StringField,TextAreaField,SubmitField,ValidationError
from wtforms.validators import Email,Required
from flask_login import current_user
from ..models import User

class PostForm(Form):
    title = StringField('Title',[validators.DataRequired()])
    content = TextAreaField('Content', [validators.DataRequired()])
    photo = FileField()
class UpdateProf(FlaskForm):
    username =StringField('Enter You Name',validators =[Required()])
    email =StringField('Enter You Email',validators =[Required(),Email()])
    bio =TextAreaField('Write a brief about yourself',validators =[Required()])
    image_file= FileField('profile picture',validators =[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
    