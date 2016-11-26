from django.test import TestCase, Client
from django.contrib.auth.models import User
from models.Author import Author
from frontEndViews import BefriendView

class FrontEndViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        author_user = User.objects.create_user(username="auth", password="secure1234")
        author_user.save()
        self.author = Author.create(user=author_user, host="localhost", displayName="auth")
        self.author.save()
        self.client.login(username=author_user.username, password="secure1234")

    def test_logged_in_user_is_available(self):
        response = self.client.post('/frontend/befriend/', json={"this is not friend json":"and will not make you any friends"})
        self.assertEqual(400, response.status_code)
