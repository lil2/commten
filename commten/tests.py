# from django.test import TestCase, LiveServerTestCase
# from selenium import webdriver
#
# # Create your tests here.
#
#
# class MyTest(LiveServerTestCase):
#     def test_home_page(self):
#         result = self.client.get('/posts/')
#         self.assertEqual(result.status_code, 302)

from django.db import connection
from django.conf import settings
def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("UPDATE django_migrations SET app = 'commten' WHERE app = 'commten';")
        row = cursor.fetchone()

    return row

if __name__ == '__main__':
    settings.configure()
    my_custom_sql()