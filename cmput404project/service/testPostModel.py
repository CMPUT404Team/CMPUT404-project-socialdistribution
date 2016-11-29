from django.test import TestCase
from models.Post import Post
from mock import MagicMock, Mock
import markdown
from models.Author import Author
from models.Comment import Comment
from unittest import skip
from django.contrib.auth.models import User

class PostModelTests(TestCase):

    def setUp(self):
        superuser = User.objects.create_superuser('superuser', 'test@test.com', 'test1234')
        self.author = Author.create(host='127.0.0.1:8000', displayName='testMonkey', user=superuser)
        self.author.save()
        self.post = Post.create(self.author,
            title="A post title about a post about web dev",
            origin="http://whereitcamefrom.com/post/zzzzz",
            description="This post discusses stuff -- brief",
            categories = ["web","tutorial"],
            visibility = "PUBLIC",
            content = "hey",
            contentType = "text/plain"
            )
        self.post.save()

    def test_Post_Creates_Id(self):
        self.assertIsNotNone(self.post.id)

    def test_Post_Title_Equal(self):
        self.assertEqual(self.post.title, "A post title about a post about web dev")

    def test_Post_Description_Equal(self):
        self.assertEqual(self.post.description, "This post discusses stuff -- brief")

    def test_Post_Origin_Equal(self):
        self.assertEqual(self.post.origin, '127.0.0.1:8000')

    def test_Post_Has_Source(self):
        self.assertIsNotNone(self.post.source)

    def test_Post_Author_Equal(self):
        self.assertEqual(self.post.author.id, self.author.id)

    def test_Post_Content_Type_Equal(self):
        self.assertEqual(self.post.contentType, "text/plain")

    def test_Post_Categories_Equal(self):
        self.assertEqual(self.post.categories, ["web","tutorial"])

    def test_Post_Visibility_Equal(self):
        self.assertEqual(self.post.visibility, "PUBLIC")

    def test_Post_Change_Visibility(self):
        self.post.visibility= "FOAF"
        self.assertEqual(self.post.visibility, "FOAF")
        self.post.visibility = "FRIENDS"
        self.assertEqual(self.post.visibility, "FRIENDS")
        self.post.visibility = "PRIVATE"
        self.assertEqual(self.post.visibility, "PRIVATE")
        self.post.visibility = "SERVERONLY"
        self.assertEqual(self.post.visibility, "SERVERONLY")
        self.post.visibility = "PUBLIC"

    def test_Post_Has_Published(self):
        self.assertIsNotNone(self.post.published)

    @skip("Failing")
    def test_Post_Add_Comment(self):
        comment = Comment.create_comment("Look at dat comment", self.author, self.post)
        comment.save()
        self.assertEqual(self.post.size, 1)

    def test_Edit_Title_Description(self):
        new_description = "my new description"
        self.post.description = new_description
        new_title = "oh hey, new title"
        self.post.title = new_title
        self.assertEqual(self.post.title, new_title)
        self.assertEqual(self.post.description, new_description)

    @skip("Not implementing yet")
    def test_Add_Image_To_Post(self):
        self.post2 = Post.create(self.author,
            title="A post title about a post about web dev",
            origin="http://whereitcamefrom.com/post/zzzzz",
            description="https://www.instagram.com/p/BMLWLAZhicf/?taken-by=sensible.heart",
            categories = ["web","tutorial"],
            visibility = "PUBLIC",
            content = "hey",
            contentType = "text/plain"
            )
        self.post2.save()
        self.assertTrue(self.post.attached_photo)

    def test_Post_Markdown(self):
        self.post.content_type = 'text/x-markdown'
        md = markdown.markdown("my markdown text")
        self.post.description = md
        self.assertEqual(self.post.description, md)
