from flask import render_template,url_for,request,flash,redirect,abort
from app.main  import main
from app.models import User,Post,Comments,Subscriber
from .. import db,photos
from .forms import UpdateProf,PostForm
from flask_login import login_required,current_user
import secrets
import os
from PIL import Image
from flask_login import login_required,login_user, current_user, logout_user


@main.route('/')
def index():
    
    page = request.args.get('page',1, type = int )
    posts = Post.query.order_by(Post.date_pub.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', posts=posts)

@main.route('/addpost',methods=['POST','GET'])
@login_required
def addpost():
    form = PostForm(request.form)
    if request.method =="POST" and form.validate():
        photo = save_pic(request.files.get('photo'))
        post = Post(title=form.title.data, body=form.content.data,category=request.form.get('category'),image=photo,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been added ','success')
        return redirect(url_for('admin'))
    return render_template('admin/addpost.html', form=form) 
@main.route('/update/<int:id>',methods=['POST','GET'])
@login_required
def update(id):
    form = PostForm(request.form)
    post = Post.query.get_or_404(id)
    form.title.data = post.title 
    form.content.data = post.body
    if request.method=='POST' and form.validate():
        if request.files.get('photo'):     
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/'+ post.image))
                post.image = save_pic(request.files.get('photo'))
            except:
                post.image = save_pic(request.files.get('photo'))
        post.title = form.title.data
        post.body = form.content.data
        post.category = request.form.get('category')
        flash('Post has been updated', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('admin/addpost.html', form=form, post=post)       

def save_pic(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join('app/static/photos', picture_filename)

    output_size = (80,80)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_filename  

@main.route('/profile',methods=['GET','POST'])
def profile():
    form = UpdateProf()
    if form.validate_on_submit():
        if form.profile_pic.data:
            picture_file= save_pic(form.image_file.data)
            current_user.profile_pic_path = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Succesfully updated your profile')
        return redirect(url_for('main.profile'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    image_file = url_for('static', filename='photos/' + current_user.image_file)   
    return render_template('profile/profile.html',image_file=image_file,title='Account',form=form)     
@main.route('/post/<id>')
def comment(id):
    comments = Comments.query.filter_by(post_id=id).all()
    post = Post.query.get(id)
    return render_template('post.html',post=post,comments=comments)    