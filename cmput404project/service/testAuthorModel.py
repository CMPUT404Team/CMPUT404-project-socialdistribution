from django.test import TestCase
from models.Author import Author
from django.contrib.auth.models import User

class AuthorModelTests(TestCase):

    def setUp(self):
        self.author = Author(user=User(username='test'))

    def test_Author_Creates_iden_field(self):
        self.assertIsNotNone(self.author.iden)
    
    def test_Author_Creates_Image_Url(self):
        self.fail()

    def test_Author_username(self):
        self.assertEqual(str(self.author), 'test')

    def test_Author_Host(self):
        self.fail()
