from django.test import TestCase
from models.Post import Post
from mock import MagicMock, Mock
import markdown
from models.Author import Author

class PostModelTests(TestCase):

    def setUp(self):
        self.author = Author(host='127.0.0.1:8000')
        self.post = Post.create(self.author,
            title="A post title about a post about web dev",
            origin="http://whereitcamefrom.com/post/zzzzz",
            description="This post discusses stuff -- brief",
            categories = ["web","tutorial"],
            visibility = "PUBLIC")
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

    def test_Post_Has_Timestamp(self):
        self.assertIsNotNone(self.post.timestamp)

    def test_Post_Comment_Count(self):
        self.assertEqual(self.post.comments.length, 0)

    def test_Post_Add_Comment(self):
        comment = Mock()
        comment.comment = "comment info"
        comment.author = self.author
        self.post.add_comment(comment)
        self.assertEqual(self.post.comments.length,1)
        self.assertEqual(self.post.comments.first(), comment)
        self.post.comments.clear()

    def test_Post_Add_Empty_Comment(self):
        comment = Mock()
        comment.comment = ""
        comment.author = self.author
        self.post.add_comment(comment)
        self.assertEqual(self.post.comments.length,0)
        self.assertNone(self.post.comments.first())
        self.post.comments.clear()

    def test_Post_Next_Equal(self):
        post_next = "http://service/posts/" + self.post.id +"/comments"
        self.assertEqual(self.post.next, post_next)

    def test_Post_Number_Of_Comments_To_Display(self):
        self.assertIsNotNone(self.post.comment_size)

    def test_Edit_Title_Description(self):
        new_description = "my new description"
        self.post.description = new_description
        new_title = "oh hey, new title"
        self.post.title = new_title
        self.assertEqual(self.post.title, new_title)
        self.assertEqual(self.post.description, new_description)

    def test_Add_Image_To_Post(self):
        image_link = "https://www.instagram.com/p/BMLWLAZhicf/?taken-by=sensible.heart"
        self.post.add_photo(image_link)
        self.assertTrue(self.post.attached_photo)

    def test_Post_Markdown(self):
        self.post.content_type = 'text/x-markdown'
        md = markdown.markdown("my markdown text")
        self.post.description = md
        assertEqual(self.post.description, md)
