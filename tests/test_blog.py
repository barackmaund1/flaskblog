import unittest
from app.models  import User,Post
from app import db

class BlogTest(unittest.TestCase):
    def setUp(self):
        self.user_albert = User(username="albert",pass_secure="albert",email="albert@yahoo.com")
        self.new_post = Post(id="1",title="testing",content="testing blog",user_id=self.user_albert)
    def tearDown(self):
        Post.query.delete()
        User.query.delete()

    def test_check_instance(self):
        self.assertEquals(self.new_post.title, 'testing')  
        self.assertEquals(self.new_post.content, 'testing blog')   
        self.assertEquals(self.new_post.user_id,self.user_albert)

    def test_save_post(self):
        self.new_post.save_blog()
        self.assertTrue(len(Post.query.all()> 0))

    def test_get_post(self):
        self.new_post.save_blog()
        g_blog = Post.get_blog(1)
        self.assertTrue(g_blog is not None)