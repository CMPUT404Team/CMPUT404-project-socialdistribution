from django.test import TestCase
from models.Author import Author
from django.contrib.auth.models import User

class AuthorModelTests(TestCase):

    def setUp(self):
        self.author = Author.create(user=User(username='test'), host='localhost')

    def test_Author_Creates_iden_field(self):
        self.assertIsNotNone(self.author.iden)
    
    def test_Author_Creates_Image_Url(self):
        self.assertNotEqual(self.author.image, '')

    def test_Author_username(self):
        self.assertEqual(str(self.author), 'test')

    def test_Author_Host(self):
        self.assertEqual(self.author.host, 'localhost')
