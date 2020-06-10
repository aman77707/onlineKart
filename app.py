import os
from flask import Flask, request, abort, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Product, Category, User, UserProduct
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    Set up CORS. Allow '*' for origins.
    '''
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    
    def updateField(field, jsonObj ,jsonKey):
        return field if jsonObj.get(jsonKey, None) is None else jsonObj.get(jsonKey)

    '''
    Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST,  PATCH , DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return "Hello!! Welcome to onlineKart"

    @app.route('/categories', methods=['POST'])
    @requires_auth('post:categories')
    def post_category(jwt):             
        data = request.get_json()
        name = data.get('name', None)

        if name is None:
            abort(400)
        
        try:
            category = Category(name=name)
            category.insert()
        except:
            abort(422)

        return jsonify({
            'success' : True,
            'category_name' : name,
            'message' : 'Successfully Inserted in the database'
            })

    @app.route('/categories/<int:category_id>', methods=['PATCH'])
    @requires_auth('patch:categories')
    def patch_category(jwt,category_id):             
        data = request.get_json()
        name = data.get('name', None)

        if name is None:
            abort(400)

        category = Category.query.filter(Category.id == category_id).one_or_none()
        if category is None:
            abort(404)
        
        try:
            category.name = name
            category.update()
        except:
            abort(422)

        return jsonify({
            'success' : True,
            'category_name' : name,
            'message' : 'Successfully Updated in the database'
            })

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()

        if categories is None:
            abort(404)

        return jsonify({
            "success" : True,
            "categories" : [c.format() for c in categories]
            })

    @app.route('/categories/<int:category_id>',methods=['DELETE'])
    @requires_auth('delete:categories')
    def delete_category(jwt, category_id):
        category = Category.query.filter(Category.id == category_id).one_or_none()
        if category is None:
            abort(404) 

        formatted_cat = category.format()
        print(formatted_cat)
        try:
            print("before deleting")
            category.delete()
            print("after deleting")

            return jsonify({
                'message' : "Deleted Successfully",
                'id' : category_id
            })
        except:
            abort(422)

    @app.route('/products', methods=['POST'])
    @requires_auth('post:products')
    def post_product(jwt): 
        data = request.get_json()
        category = data.get('category', None)
        name = data.get('name', None)
        price = data.get('price', None)
        description = data.get('description', None)
        availability_status = data.get('availability_status', None)

        try:
            product = Product(category_id=category, name=name, price=price, availability_status=availability_status, description=description)
            product.insert()
        except:
            abort(422)

        return jsonify({
            'success' : True,
            'name' : name,
            'category_id' : category,
            'price' : price,
            'availability_status' : availability_status,
            'description' : description
            })

    @app.route('/products/<int:product_id>', methods=['PATCH'])
    @requires_auth('patch:products')
    def patch_product(jwt,product_id):  
        data = request.get_json()
        product = Product.query.filter(Product.id == product_id).one_or_none()

        if product is None:
            abort(404)

        try:
            product.category = data.get('category', None)
            product.name = data.get('name', None)
            product.price = data.get('price', None)
            product.description = data.get('description', None)
            product.availability_status = data.get('availability_status', None)
            product.update()

        except:
            abort(422)

        return jsonify({
            'success' : True,
            'name' : product.name,
            'category_id' : product.category,
            'price' : product.price,
            'availability_status' : product.availability_status,
            'description' : product.description
            })


    @app.route('/products', methods=['GET'])
    def get_products():
    	products = Product.query.order_by(Product.id).all()

    	if products is None:
    		return "Sorry!! No records found"
    	return jsonify({
    		"success" : True,
    		"products" : [p.format() for p in products]
    		})

    @app.route('/products/<int:product_id>',methods=['DELETE'])
    @requires_auth('delete:products')
    def delete_product(jwt, product_id):
        product = Product.query.filter(Product.id == product_id).one_or_none()
        if product is None:
            abort(404)                                                                                                                                
        try:
    
            product.delete()

            return jsonify({
                'message' : "Deleted Successfully",
                'id' : product_id
            })
        except:
            abort(422)

    @app.route('/users', methods=['GET'])
    @requires_auth('get:users')
    def get_users(jwt):
        users = User.query.order_by(User.id).all()

        if users is None:
            abort(404)

        return jsonify({
            "success" : True,
            "users" : [u.format() for u in users]
            })

    @app.route('/users', methods=['POST'])
    @requires_auth('post:users')
    def post_user(jwt):             
        data = request.get_json()
        name = data.get('name', None)

        if name is None:
            abort(400)
        
        try:
            user = User(name=name)
            user.insert()
        except:
            abort(422)

        return jsonify({
            'success' : True,
            'user_name' : name,
            'message' : 'Successfully Inserted in the database'
            })

    @app.route('/users/<int:user_id>',methods=['DELETE'])
    @requires_auth('delete:users')
    def delete_user(jwt,user_id):
        user = User.query.filter(User.id == user_id).one_or_none()
        if user is None:
            abort(404)                                                                                                                                
        try:
    
            user.delete()

            return jsonify({
                'message' : "Deleted Successfully",
                'id' : user_id
            })
        except:
            abort(422)

    @app.route('/purchase', methods=['POST'])
    @requires_auth('post:transaction')
    def new_purchase(jwt):             
        data = request.get_json()
        user_id = data.get('user_id', None)
        product_id = data.get('product_id', None)

        if user_id is None:
            abort(400)

        if product_id is None:
            abort(400)
        
        try:
            product = Product.query.filter(Product.id == product_id).one_or_none()

            if product is None or product.availability_status is False:
                abort(404)
            user_product = UserProduct(user_id=user_id, product_id=product_id)
            user_product.insert()

        except:
            abort(422)

        return jsonify({
            'success' : True,
            'user_id' : user_id,
            'product_id' : product_id,
            'message' : 'Thankyou for shopping with us!!'
            })

    @app.route('/transactions', methods=['GET'])
    @requires_auth('get:transactions')
    def get_all_transactions(jwt):
        users_products = UserProduct.query.all()

        if users_products is None:
            abort(404)

        return jsonify({
            "success" : True,
            "userproducts" : [u.format() for u in users_products]
            })


    '''
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
     
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Resource not found"
            }), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify({
            "success": False, 
            "error": 403,
            "message": "Forbidden from accessing the resource"
            }), 403 

    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({
            "success": False, 
            "error": 401,
            "message": "Unauthorized"
            }), 401


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable"
            }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "Method not allowed"
            }), 405

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Bad request"
            }), 400

    return app

app = create_app()
if __name__ == '__main__':
    app.run()

    
