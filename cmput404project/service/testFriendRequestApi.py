from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from unittest import skip
from models.Author import Author
import json

class FriendRequestApiTest(APITestCase):
    
    def setUp(self):
	self.user = User.objects.create_user('user', 'test@test.com', 'test1234')
        self.client = APIClient()
        #Authenticate as a super user so we can test everything
        self.client.force_authenticate(user=self.user)  
        self.friend_request_url = reverse("friend-request")

    def test_only_post_method_allowed(self):
        # make sure 405 is returned
        self.assertEqual(405, self.client.get(self.friend_request_url).status_code)
        self.assertEqual(405, self.client.put(self.friend_request_url).status_code)
        self.assertEqual(405, self.client.delete(self.friend_request_url).status_code)
        self.assertEqual(405, self.client.head(self.friend_request_url).status_code)

    def test_should_return_401_on_not_logged_in(self):
        not_logged_in_client = APIClient()
        self.assertEqual(401, not_logged_in_client.post(self.friend_request_url).status_code)

    @skip("NI")
    def test_should_400_on_not_json(self):
        self.fail()

    def test_should_add_friend(self):
        author = Author.create(self.user, 'testMonkey', 'local') 
        author.save()
        friend = Author.create(User.objects.create_user(username='tester2', password='test1234'), 'banana', 'local')
        friend.save()
        post_data = {
            "query":"friendrequest",
            "author": {
                    "id":str(author.id),
                    "host":author.host,
                    "displayName": author.displayName
            },
            "friend": {
                    "id":str(friend.id),
                    "host":friend.host,
                    "displayName":friend.displayName,
                    "url":friend.host+"/author/"+str(friend.id)
            }
        } 
        self.client.force_authenticate(user=author.user)
        response = self.client.post(self.friend_request_url, data=post_data, format='json')
        self.assertEqual(204, response.status_code, response.data)
        try:
            friend_id_from_author = author.friends.get(id=friend.id).id
        except Author.DoesNotExist:
            self.fail("The friend was not added to the author")

    @skip("Not Implemented")
    def test_should_400_if_friend_does_not_exist(self):
        self.fail()
    @skip("Not Implemented")
    def test_should_400_if_author_does_not_exist(self):
        self.fail()
    @skip("Not Implented")
    def test_should_only_accept_json(self):
        self.fail()
