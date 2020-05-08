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
    profile_pic = FileField('profile picture',validators =[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
@app.route('/addpost',methods=['POST','GET'])
@login_required
def addpost():
    form = PostForm(request.form)
    if request.method =="POST" and form.validate():
        photo = save_photo(request.files.get('photo'))
        post = Post(title=form.title.data, body=form.content.data,category=request.form.get('category'),image=photo,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been added ','success')
        return redirect(url_for('admin'))
    return render_template('admin/addpost.html', form=form)

    def validate_email(self,email):
        if email.data != current_user.email:
            if User.query.filter_by(email = email.data).first():
                raise ValidationError("The Email has already been taken!")
    def validate_username(self,username):
        if username.data != current_user.username:
            if User.query.filter_by(username = username.data).first():
                raise ValidationError("The username has already been taken")    