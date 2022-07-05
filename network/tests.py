import json
from multiprocessing.connection import Client
from django.test import TestCase
from django.urls import reverse
from .models import *


# Create your tests here.
class NetworkTestCase(TestCase):

    def setUp(self):
        # Create User
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username="testuser", password="12345")

    # test post object
    def test_post(self):
        Post.objects.create(sender=self.user, content="test_content")
        all = Post.objects.all()
        self.assertTrue(len(all) == 1)
        post = Post.objects.get(pk=1)
        self.assertTrue(post is not None)
