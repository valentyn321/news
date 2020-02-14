from django.test import TestCase, Client
from django.urls import reverse
from main.models import Post, Comment
import json

class TestViews(TestCase):

	def setUp(self):
		self.client = Client()
		self.news_list_url = reverse('news_list')

	def test_news_list_GET(self):
		
		response = self.client.get(self.news_list_url)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/news_list.html')

