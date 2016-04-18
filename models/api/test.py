from django.test import TestCase, Client, LiveServerTestCase
from django.db import IntegrityError
from models.models import User, Tag, ItemCategory, Item, Comment,Authenticator

from django.contrib.auth.models import User, Group

import json

class ApiTestCase(TestCase):
    fixtures = ['fixtures']

    def setup(self):
    	c = Client()
    	u1 = models.User(username='test',                         \
                    email="test@test",                               \
                    phone='1234567',                               \
                    password=hashers.make_password('testpassword'),  \
                    )
    	u1.save()
	

	def test_create_user_get(self):
		response = c.get('api/v1/users/create')
		self.assertTrue("must make POST request" in respone)


	def test_create_user_post_missing_feilds(self):
		response = c.post('api/v1/users/create', {'username' : 'jsd2ej', 'email': 'test@email.com', 'password' : '123'}) 
 		self.assertTrue("missing required fields" in respone)


	def test_create_user_post(self):
		response = c.post('api/v1/users/create', {'username' : 'jsd2ej', 'email': 'test@email.com', 'password' : '123', 'phone' : '1234567'}) 
 		self.assertTrue("user_id" in respone)

 	def test_find_user_get(self):
 		respone = c.get('api/v1/users/-1')
 		self.assertTrue("user not found" in respone)

 	def test_find_user_get_success(self):
 		respone = c.get('api/v1/users/1')
 		self.assertTrue("Aaron" in respone)

 	def test_update_user(self):
 		respone = c.post('api/v1/users/1/update', {
 				'username'='test1',                         \
                'email'="test1@test",                               \
                'phone'='1234567',                               \
                'password':'testpasswor1d'  
                })
 		self.assertTrue('ok' in respone)

 	def test_find_item(self):
 		respone = 
 	