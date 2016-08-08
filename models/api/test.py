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
        c = Client()
        response = c.get('/api/v1/users/create')
        print( response)
        self.assertTrue("must make POST request" in response)

    def test_create_user_post_missing_feilds(self):
        c = Client()
        response = c.post('api/v1/users/create', {'username' : 'jsd2ej', 'email': 'test@email.com', 'password' : '123'}) 
        self.assertTrue("missing required fields" in response)


    def test_create_user_post(self):
        c = Client()
        response = c.post('/api/v1/users/create', {'username' : 'jsd2ej', 'email': 'test@email.com', 'password' : '123', 'phone' : '1234567'}) 
        self.assertTrue("user_id" in response)

    def test_find_user_get(self):
        c = Client()
        response = c.get('/api/v1/users/1000')
        self.assertTrue("user not found" in response)

    def test_find_user_get_success(self):
        c = Client()
        response = c.get('/api/v1/users/1')
        self.assertTrue("Aaron" in response)

    def test_update_user(self):
        c = Client()
        response = c.post('/api/v1/users/1/update', {
                        'username':'test1',                         \
                        'email':"test1@test",                               \
                        'phone':'1234567',                               \
                        'password':'testpasswor1d'  
                          })
        self.assertTrue('ok' in response)
    
    def test_create_item_get(self): 
        c = Client()
        response = c.get ('/api/v1/items/create')
        self.assertTrue('must make POST request' in response)
        
    def test_create_item_post_bad(self):
        c = Client()
        response = c.post('/api/v1/items/create', {
                'owner':'1',
                'title' : 'Test Title',
                'description' : 'Test DISCRIPTIONS LALALALALLALALL',
                'filename': 'TestFile',
                'size':'2gb',
                'tags': '8'
            })
        self.assertTrue('missing required fields' in response)

    def test_create_item_post_no_owner(self):
        c = Client()
        response = c.post('/api/v1/items/create', {
                'owner':'1000',
                'title' : 'Test Title',
                'description' : 'Test DISCRIPTIONS LALALALALLALALL',
                'filename': 'TestFile',
                'size':'2gb',
                'tags': '8',
                'category':'9'
            })
        self.assertTrue('user not found' in response)

     def test_create_item_post_good(self):
        c = Client()
        response = c.post('/api/v1/items/create', {
                'owner':'1',
                'title' : 'Test Title',
                'description' : 'Test DISCRIPTIONS LALALALALLALALL',
                'filename': 'TestFile',
                'size':'2gb',
                'tags': '8',
                'category':'9'
            })
        self.assertTrue('item_id' in response)

    def test_find_item_post(self):
        c = Client()
        response = c.post('/api/v1/items/10')
        self.assertTrue('must make GET request' in response)

    def test_find_item_get_not_found(self):
        c = Client()
        response = c.get('/api/v1/items/10000')
        self.assertTrue('item not found' in response)


    def test_find_item_get_found(self):
        c = Client()
        response = c.get('/api/v1/items/10')
        self.assertTrue('owner' in response)
    
    def test_find_items_user_post(self):
        c = Client()
        response = c.post('/api/v1/items/getItemsUserid')
        self.assertTrue('must make GET request' in response)

    def test_find_items_user_get_not_found_user(self):
        c = Client()
        response = c.get('/api/v1/items/getItemsUserid')
        self.assertTrue('user not found' in response)

    def test_find_items_user_get_found_user(self):
        c = Client()
        response = c.get('/api/v1/items/getItemsUserid', {'user_id':1})
        self.assertTrue('items' in response)

    def test_update_item_post_not_found(self):
        c = Client()
        response = c.post('/api/v1/items/10000/update')
        self.assertTrue('item not found' in response)

    def test_update_item_post_user_not_found(self):
        c = Client()
        response = c.post('/api/v1/items/10/update',{
                'owner' : 10000
            })
        self.assertTrue('user not found' in response)

    def test_update_item_post_found(self):
        c = Client()
        response = c.post('/api/v1/items/10/update',{
                'title' : 'New Title'
            })
        self.assertTrue('ok' in response)

    def test_get_all_items_post(self):
        c = Client()
        response = c.post('/api/v1/items/getAllItems',{
                'badPost' : 'Bad'
            })
        self.assertTrue('must make GET request' in response)

    def test_get_all_items_get(self):
        c = Client()
        response = c.get('/api/v1/items/getAllItems')
        self.assertTrue('items' in response)
    
    def test_get_recent_recent_post(self):
        c = Client()
        response = c.post('/api/v1/items/getRecent/3',{
                'badPost' : 'Bad'
            })
        self.assertTrue('must make GET request' in response)

    def test_get_recent_recent_get_negitve_number(self):
        c = Client()
        response = c.get('/api/v1/items/getRecent/-3')
        self.assertTrue('Must be positive integer' in response)

    def test_get_recent_recent_get_negitve_number(self):
        c = Client()
        response = c.post('/api/v1/items/getRecent/3')
        self.assertTrue('items' in response)

    def test_add_comment_get(self):
        c = Client()
        response = c.get('/api/v1/items/10/comment')
        self.assertTrue('must make POST request' in request)

    def test_add_comment_post_missing(self):
        c = Client()
        response = c.post('/api/v1/items/10/comment', {
            'owner' : '1'
            })
        self.assertTrue('missing required fields' in request)

    def test_add_comment_post_user_not_found(self):
        c = Client()
        response = c.post('/api/v1/items/10/comment', {
            'owner' : '10000',
            'text' : 'TEsst text comment'
            })
        self.assertTrue('user not found' in request)

    def test_add_comment_post_item_not_found(self):
        c = Client()
        response = c.post('/api/v1/items/1000/comment', {
            'owner' : '1',
            'text' : 'TEsst text comment'
            })
        self.assertTrue('item not found' in request)

    def test_add_comment_work(self):
        c = Client()
        response = c.post('/api/v1/items/10/comment', {
            'owner' : '1',
            'text' : 'TEsst text comment'
            })
        self.assertTrue('comment_id' in request)

    def test_find_comment_post(self):
        c = Client()
        response = c.post('/api/v1/comments/11', {
            'badPost' : '1'
            })
        self.assertTrue('must make GET request' in request)

    def test_find_comment_get_comment_not_found(self):
        c = Client()
        response = c.get('/api/v1/comments/111')
        self.assertTrue('comment not found' in request)

    def test_find_comment_get_comment_found(self):
        c = Client()
        response = c.get('/api/v1/comments/11')
        self.assertTrue('owner' in request)

    def test_update_comment_get(self):
        c = Client()
        response = c.get('/api/v1/comments/11/update')
        self.assertTrue('must make POST request' in request)

    def test_update_comment_post_not_found_comment(self):
        c = Client()
        response = c.post('/api/v1/comments/111/update',{
            'owner': '1',
            'item':'1',
            'text':'New Comment Text'})
        self.assertTrue('comment not found' in request)

    def test_update_comment_post_not_found_user(self):
        c = Client()
        response = c.post('/api/v1/comments/11/update',{
            'owner': '122',
            'item':'1',
            'text':'New Comment Text'})
        self.assertTrue('user not found' in request)

    def test_update_comment_post_not_found_user(self):
        c = Client()
        response = c.post('/api/v1/comments/11/update',{
            'owner': '1',
            'item':'122',
            'text':'New Comment Text'})
        self.assertTrue('item not found' in request)

    def test_update_comment_post_work(self):
        c = Client()
        response = c.post('/api/v1/comments/11/update',{
            'owner': '1',
            'item':'1',
            'text':'New Comment Text'})
        self.assertTrue('ok' in request)

    def test_create_auth_get(self):
        c = Client()
        response = c.get('/api/v1/auth/create')
        self.assertTrue('must make POST request' in request)

    def test_create_auth_post_no_id(self):
        c = Client()
        response = c.post('/api/v1/auth/create',{
            'BadPost':'badpost'})
        self.assertTrue('missing user id' in request)

    def test_create_auth_post_work(self):
        c = Client()
        response = c.post('/api/v1/auth/create',{
            'user_id':'1'})
        self.assertTrue('ok' in request)

    
    def test_delete_auth_post(self):
        c = Client()
        response = c.post('/api/v1/auth/delete',{
            'BadPost':'badpost'})
        self.assertTrue('must make GET request' in request)

    def test_delete_auth_get_work(self):
        c = Client()
        response = c.get('/api/v1/auth/delete',{
            'auth_key' :'5617108875896112008651696229316812319686481185424272387784195962675048408556309662724663664030875369'})
        self.assertTrue('auth_deleted' in request)

    def test_delete_auth_get_not_found(self):
        c = Client()
        response = c.get('/api/v1/auth/delete')
        self.assertTrue('must provide auth key' in request)









