from django.test import TestCase
from models.Author import Author
from django.contrib.auth.models import User

class AuthorModelTests(TestCase):

    def setUp(self):
        self.author = Author(host='localhost', displayName='test')

    def test_Author_Creates_Id(self):
        self.assertIsNotNone(self.author.id)
    
    def test_Author_Username(self):
        self.assertEqual(self.author.displayName, 'test')

    def test_Author_Host(self):
        self.assertEqual('localhost',self.author.host)
    
    def test_Author_Friend(self):
        friend = Author()
        self.author.add_friend(friend)
        self.assertEqual(friend, self.author.friends.first())
