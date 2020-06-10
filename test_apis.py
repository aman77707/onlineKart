import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Product, Category, User, UserProduct


class OnlineKartTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        self.adminToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikt4R0xFbGtMZHVyREd0QXZjemFfWiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYXBzdG9uZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkNjdmNWMxZTI3MWQwYmU4YzZlYmQ3IiwiYXVkIjoib25saW5lS2FydEFwaSIsImlhdCI6MTU5MTcxMTUyOCwiZXhwIjoxNTkxNzk3OTI2LCJhenAiOiJjQzJsOGZCbDVUc3U3ZTVuT29LY2liUklGOWFlcHJQQyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmNhdGVnb3JpZXMiLCJkZWxldGU6cHJvZHVjdHMiLCJkZWxldGU6dXNlcnMiLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDpwcm9kdWN0cyIsImdldDp0cmFuc2FjdGlvbnMiLCJnZXQ6dXNlcnMiLCJwYXRjaDpjYXRlZ29yaWVzIiwicGF0Y2g6cHJvZHVjdHMiLCJwb3N0OmNhdGVnb3JpZXMiLCJwb3N0OnByb2R1Y3RzIiwicG9zdDp1c2VycyJdfQ.puUVU-dQF3iTZerKdbDYBZ9BAaV9IPvi83W9FvooD0WVm4u4IgF6dPPNdC0sM0lVXdRaxnv6JUAE5303eJkgoZwKtEjKaWMdx7jFQrLAunm1mHovWW9U-4bYWGDKN7Mj-QA09nAFS6b_3uWNcs3RzpMgbBYqFJN4Ok5eVvQux2Ig4Ymd7uXhpCikDHG3Mcz5rxgPdKlFNXJATsXYkeeHqsButk9_pzdPryRIF0Bn5ZgqNV1h94N1FZsL8kV6n4YyQF_cr9-svP1XpjIkP7O74a-5ZhIzEElDuavOsmZWUEKGNGTWxCPfPYCkKLXeUjCvnC8JGOWNVLSfMeUpASwE0Q'
        self.customerToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikt4R0xFbGtMZHVyREd0QXZjemFfWiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYXBzdG9uZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkYjI5NmYyMjlkY2UwMDEzZDUzZDU3IiwiYXVkIjoib25saW5lS2FydEFwaSIsImlhdCI6MTU5MTcxMTYxNSwiZXhwIjoxNTkxNzk4MDEzLCJhenAiOiJjQzJsOGZCbDVUc3U3ZTVuT29LY2liUklGOWFlcHJQQyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmNhdGVnb3JpZXMiLCJnZXQ6cHJvZHVjdHMiLCJwb3N0OnRyYW5zYWN0aW9uIl19.YdY0JLcSjHfJsTPV3rG3p3OwhA6FDhbnJB0zNtkcooIbHYKXY2u7KvAzlrvMAQTKxG3F41WIQlcBJjT2n2IfRqB1JwowrSd1PN8N-Hfz9XMfOBHyMSm2LU8RyM-gEbGMzONFpf_a-d-GIKY-TbAEESDzm3YIvuXhYW_aS7y79hUeE0qlTHq3gER47EZRR4ufoL7RTgcPruHtO824_dF_dnvGdXm1Q3l6O81u9ixIwMtL1MEa53hfeI0Mdav_dgCL82dEKLK7um-zT_suAzNZyecIdxX6ON8LVVu6O7IgC83aJcTU-Pw73lzsWs1olg2N8JVQjo5lIXTpI4O_meyu2w'

        self.new_category = {
                "name" : "electronics"
        }
        self.new_category_wrong = {
                "name_wrong" : "electronics"
        }
        self.new_product = {
                "name" : "trimmer", 
                "category" : 1 , 
                "price" : 1120, 
                "description": "Grooming appliance" , 
                "availability_status" : True
        }
        self.new_product_wrong = {
                "name" : "trimmer", 
                "category" : None , 
                "price" : "1120", 
                "description": "Grooming appliance" , 
                "availability_status" : 456
        }
        self.new_user= {
                "name" : "Aman Bhardwaj" 
        }
        self.new_user_wrong= {
                "name_wrong" : 'Dummy Name' 
        }
        self.new_transaction = {
                "user_id" : 4,
                "product_id" : 3
        }

    def tearDown(self):
        """Executed after reach test"""
        transaction = UserProduct.query.filter(UserProduct.user_id == 1).one_or_none()
        if transaction is not None:
            transaction.delete()
        pass
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_posting_new_category_success(self):                                                                                                              
        """Test _____________ """
        res = self.client().post('/categories', headers={'Authorization': 'Bearer ' +self.adminToken},json=self.new_category)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['category_name'], 'electronics')

    def test_posting_new_category_error_400(self):                                                                                                              
        """Test _____________ """
        res = self.client().post('/categories', headers={'Authorization': 'Bearer ' +self.adminToken},json=self.new_category_wrong)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_patching_new_category_success(self):                                                                                                              
        """Test _____________ """
        res = self.client().patch('/categories/1', headers={'Authorization': 'Bearer ' +self.adminToken},json={'name' : 'groceries'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['category_name'], 'groceries')

    def test_patching_new_category_error_404(self):                                                                                                              
        """Test _____________ """
        res = self.client().patch('/categories/1000', headers={'Authorization': 'Bearer ' +self.adminToken},json={'name' : 'groceries'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_patching_new_category_error_401(self):                                                                                                              
        """Test _____________ """
        res = self.client().patch('/categories/1', headers={'Authorization': 'Bearer ' +self.customerToken},json={'name' : 'groceries'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        

    def test_getting_categories(self):
        """Test _____________ """
        res = self.client().get('/categories', headers={'Authorization': 'Bearer ' +self.adminToken})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories'])) 

    def test_getting_categories_success_using_customer_token(self):
        """Test _____________ """
        res = self.client().get('/categories', headers={'Authorization': 'Bearer ' +self.customerToken})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories'])) 

    def test_deleting_category_error_404(self):                                                                                                              
        """Test _____________ """
        res = self.client().delete('/categories/10001', headers={'Authorization': 'Bearer ' +self.adminToken},json=self.new_category)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    def test_posting_new_product_success(self):                                                                                                              
        """Test _____________ """
        res = self.client().post('/products', headers={'Authorization': 'Bearer ' +self.adminToken},json=self.new_product)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['name'], 'trimmer')
        self.assertEqual(data['category_id'], 1)
        self.assertEqual(data['price'], 1120)
        self.assertEqual(data['availability_status'], True)
        self.assertEqual(data['description'],'Grooming appliance' )

    def test_posting_new_product_error_422(self):                                                                                                              
        """Test _____________ """
        res = self.client().post('/products', headers={'Authorization': 'Bearer ' +self.adminToken},json=self.new_product_wrong)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patching_new_product_success(self):                                                                                                              
        """Test _____________ """
        res = self.client().patch('/products/1', headers={'Authorization': 'Bearer ' +self.adminToken},json={'description' : 'Changed the description'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['description'],'Changed the description' )

    def test_patching_new_product_error_422(self):                                                                                                              
        """Test _____________ """
        res = self.client().patch('/products/1', headers={'Authorization': 'Bearer ' +self.adminToken},json=self.new_product_wrong)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_getting_products_success(self):                                                                                                              
        """Test _____________ """
        res = self.client().get('/products', headers={'Authorization': 'Bearer ' +self.adminToken},json=self.new_product_wrong)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['products']))

    def test_getting_products_success_using_customer_token(self):                                                                                                              
        """Test _____________ """
        res = self.client().get('/products', headers={'Authorization': 'Bearer ' +self.customerToken},json=self.new_product_wrong )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['products']))

    def test_deleting_product_error_404(self):                                                                                                              
        """Test _____________ """
        res = self.client().delete('/products/10001', headers={'Authorization': 'Bearer ' +self.adminToken},json=self.new_category)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_posting_new_user_success(self):                                                                                                              
        """Test _____________ """
        res = self.client().post('/users', headers={'Authorization': 'Bearer ' +self.adminToken},json=self.new_user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['user_name'], 'Aman Bhardwaj')

    def test_posting_new_user_error_400(self):                                                                                                              
        """Test _____________ """
        res = self.client().post('/users', headers={'Authorization': 'Bearer ' +self.adminToken},json=self.new_user_wrong)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_deleting_user_error_404(self):                                                                                                              
        """Test _____________ """
        res = self.client().delete('/users/1000', headers={'Authorization': 'Bearer ' +self.adminToken},json=self.new_user_wrong)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_getting_users_success(self):                                                                                                              
        """Test _____________ """
        res = self.client().get('/users', headers={'Authorization': 'Bearer ' +self.adminToken})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['users']))

    def test_getting_users_error_403(self):                                                                                                              
        """Test _____________ """
        res = self.client().get('/users', headers={'Authorization': 'Bearer ' +self.customerToken})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


    def test_posting_transactions_success(self):                                                                                                              
        """Test _____________ """
        res = self.client().post('/purchase', headers={'Authorization': 'Bearer ' +self.customerToken} , json={'user_id' : 1,'product_id' : 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['user_id'], 1)
        self.assertEqual(data['product_id'], 1)

    def test_posting_transactions_error_403(self):                                                                                                              
        """Test _____________ """
        res = self.client().post('/purchase', headers={'Authorization': 'Bearer ' +self.adminToken} , json={'user_id' : 1,'product_id' : 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_getting_transactions_success(self):                                                                                                              
        """Test _____________ """
        res = self.client().get('/transactions', headers={'Authorization': 'Bearer ' +self.adminToken})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['userproducts']), 0)

    def test_getting_transactions_error_403(self):                                                                                                              
        """Test _____________ """
        res = self.client().get('/transactions', headers={'Authorization': 'Bearer ' +self.customerToken})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
