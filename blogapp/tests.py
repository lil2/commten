from django.test import TestCase, LiveServerTestCase
from selenium import webdriver

# Create your tests here.


class MyTest(LiveServerTestCase):
    def test_home_page(self):
        result = self.client.get('/posts/')
        self.assertEqual(result.status_code, 200)