from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from unittest import skip

class FriendRequestApiTest(APITestCase):
    
    def setUp(self):
	user = User.objects.create_user('user', 'test@test.com', 'test1234')
        self.client = APIClient()
        #Authenticate as a super user so we can test everything
        self.client.force_authenticate(user=user)  
        self.friend_request_url = reverse("friend-request")

    def test_only_post_method_allowed(self):
        # make sure 405 is returned
        self.assertEqual(405, self.client.get(self.friend_request_url).status_code)
        self.assertEqual(405, self.client.put(self.friend_request_url).status_code)
        self.assertEqual(405, self.client.delete(self.friend_request_url).status_code)
        self.assertEqual(405, self.client.head(self.friend_request_url).status_code)

    @skip("Not Implemented")
    def test_should_return_401_on_not_logged_in(self):
        self.fail()
    @skip("Not Implemented")
    def test_should_add_friend(self):
        self.fail()
    @skip("Not Implemented")
    def test_should_400_if_friend_does_not_exist(self):
        self.fail()
    @skip("Not Implemented")
    def test_should_400_if_author_does_not_exist(self):
        self.fail()
