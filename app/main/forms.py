from wtforms import Form, StringField,FileField,  validators, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired

class PostForm(Form):
    title = StringField('Title',[validators.DataRequired()])
    content = TextAreaField('Content', [validators.DataRequired()])
    photo = FileField()