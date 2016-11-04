from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.contrib.auth.models import User
from unittest import skip

@skip("Not Implemented")
class FriendRequestApiTest(APITestCase):
    
    def setUp(self):
	user = User.objects.create_user('user', 'test@test.com', 'test1234')
        self.client = APIClient()
        #Authenticate as a super user so we can test everything
        self.client.force_authenticate(user=superuser)  

    def test_only_post_method_allowed(self):
        # make sure 405 is returned
        self.assertFail()	

    def test_should_return_401_on_not_logged_in(self):
        self.assertFail()

    def test_should_add_friend(self):
        self.assertFail()

    def test_should_400_if_friend_does_not_exist(self):
        self.assertFail()

    def test_should_400_if_author_does_not_exist(self):
        self.assertFail()
