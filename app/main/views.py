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

@main.route('/post/new',methods=['POST','GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been added ','success')
        return redirect(url_for('main.index'))
    return render_template('admin/addpost.html',title='New Post',legend='New Post', form=form) 

@main.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comments.query.filter_by(post_id=post_id).all()
    return render_template('post.html', title=post.title,comments=comments, post=post)
@main.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('admin/addpost.html', post='post',
                           form=form, legend='Update Post')


@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))      

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
        if form.image_file.data:
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
@main.route('/comment/<post_id>',methods=['GET','POST'])

def comment(post_id):
    blog = Blog.query.get(post_id)
    comment = request.form.get('newcomment')
    new_comment = Comment(comment = comment, user_id = current_user._get_current_object().id, post_id=post_id)
    new_comment.save_comment()
    return redirect(url_for('main.blog',id= post.id))
 
@main.route("/post/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comments.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('main.index'))      
