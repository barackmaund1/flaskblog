from . import db,login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.String(255))
    image_file=db.Column(db.String(20),nullable=False,default='default.jpg')
    pass_secure = db.Column(db.String(200),  nullable=False)
    post=db.relationship('Post',backref='user',lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)
    
        
    
    def __repr__(self):
        return f'User{self.username},{self.email}'  

class Post(db.Model):
    __tablename__='posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    author = db.relationship('User', backref=db.backref('posts',lazy=True))
    views = db.Column(db.Integer,default=0)
    date_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment = db.relationship('Comment', backref='post', lazy='dynamic')
    def __repr__(self):
        return '<Post %r' % self.title

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    def delete_post(self):
        db.session.add(self)
        db.session.commit()

    # @classmethod
    def get_post(self,id):
        post = Post.query.filter_by(id=id).first()
        return post


class Comment(db.Model):
    __tablename__='comments'
     
    id = db.Column(db.Integer, primary_key=True)
    comment= db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    date_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    user_id= db.Column(db.Integer,db.ForeignKey("users.id"))  

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_commit(self):
        db.session.add(self)
        db.session.commit()

    # @classmethod
    def get_comment(self,id):
        comment = Comment.query.all(id=id)
        return comment

    def __repr__(self):
        return f'Comment {self.comment}'   

class Subscriber(db.Model):
    __tablename__='subscribers'

    id=db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),unique=True,index=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))  
    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Subscriber {self.email}'

