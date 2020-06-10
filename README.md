# OnlineKart E-commerce

## Motivation:
  Motivattion for the project came from the idea of creating a basic and sample proof of concept for the      
  online shopping platform. Though the project has missing front-end and is under the scope of enormous     
  improvement it has definitely achored me at a position from where I can take this project from a sample   
  POC to a completely built working website as an e-commerce platform.  

## TechStack:  
  The application has a backend that uses these key technologies:        
  * Flask framework
  * Flask Sqlalchemy ORM
  * Flask-CORS
  * AUTH0
  * JWT 

## Dependencies and hosting instructions:
### Carry out the following steps:
  * Once, the repository has been cloned in a local environment, navigate to the repository root which contains  
    requirements.txt file and execute:  
    ```
    pip install -r requirements.txt
    ```  
  * After installing the dependencies, set flask variable FLASK_APP. To do this execute the below command:  
    ```
    export FLASK_APP=app.py
    ```
  * Set the environment variables by running the command:  
    ```
    source setup.sh
    ```
  * To run the server, run:  
    ```
    flask run --reload
    ```

  Post starting the server, we are in position to start sending requests to the end points hosted on the URL.

## Types of users in the system:
  * Admin:  
    This user has all the necessary permissions for the database tables. It is allowed to carry out the following  
    operations:  
      * Get categories
      * Post categories
      * Delete categories
      * Patch categories
      * Get Products
      * Post Products
      * Patch Products
      * Delete Products
      * Get Customers
      * Post Customers
      * Delete Customers
      * Get Transactions

  * Customer:
    This user has permissions to get the products, categories and carry out transactions to purchase the products:  
      * Get categories
      * Get Products
      * Post Transactions

  * Guest:
    This user can just view the products and categories:  
      * Get categories
      * Get Products

## Working Tokens for type of each user:  
  * Admin Token :   
  * Customer Token :  
  * Guest: Not Required  

## API Endpoints:  
  * GET: http://127.0.0.1:5000/categories  
    This endpoint is used to get a list of all the categories of products available in the store. An example of response looks like:  
    ```
    {  
          "categories": [  
          {  
            "id": 4,   
            "name": "electronic"  
          },   
          {  
            "id": 5,   
            "name": "groceries"  
          }  
        ],  
        "success" : True  
    }
    ```
    Permitted Users : Admin, Customer, Guest  
  * POST: http://127.0.0.1:5000/categories  
    This input takes a json of the category to be created as input, an example of such a category looks like:  
    ```
    {
      "name" : "electronics"
    }
    ```
    The response from such POST request would look like:  
    ```
    {
      "category_name": "electronics", 
      "message": "Successfully Inserted in the database", 
      "success": true
    }
    ``` 
    Permitted Users : Admin  
  * PATCH: http://127.0.0.1:5000/categories/<category_id>  
    This input takes a json of the category to be created as input, an example of such a category looks like:  
    ```
    {
      "name" : "electricals"
    }
    ```
    The response from such PATCH request would look like:  
    ```
    {
      "category_name": "electricals", 
      "message": "Successfully Updated in the database", 
      "success": true
    }
    ``` 
    Permitted Users : Admin  
  * DELETE: http://127.0.0.1:5000/categories/<category_id>  
    This end point deletes the mentioned category ID from the system. An example of response looks like:  
    ```
    {
      "id": 9, 
      "message": "Deleted Successfully"
    }
    ```
    Permitted Users : Admin  
  * GET: http://127.0.0.1:5000/products  
    This endpoint is used to get a list all the products of a specific category available in the store. An example of response looks like:  
    ```
    {  
      "products": [
        {
          "availability_status": true, 
          "category_id": 4, 
          "description": "Grooming appliance for men", 
          "id": 3, 
          "name": "Trimmer", 
          "price": 1120
        }
      ],  
      "success" : True  
    }
    ```
    Permitted Users : Admin, Customer, Guest  
  * POST: http://127.0.0.1:5000/products  
    This endpoint is used to add a new product in the store database. This API takes an input as a JSON object for the product to be entered:  
    ```
    {
      "name" : "trimmer", 
      "category" : 1 , 
      "price" : 1120, 
      "description": "Grooming appliance" , 
      "availability_status" : true
    }
    ```
    Response for such request looks like:
    ```
    {
      "availability_status": true, 
      "category_id": 4, 
      "description": "Grooming appliance", 
      "name": "trimmer", 
      "price": 1120, 
      "success": true
    }
    ```
    Permitted Users : Admin  
  * PATCH: http://127.0.0.1:5000/products/<product_id>  
    This endpoint is used to update the details of a product in the store database. This API takes an input as a JSON object for the product to be entered:   
    ```
    {
      "name" : "trimmer", 
      "category" : 1 , 
      "price" : 1120, 
      "description": "Grooming appliance" , 
      "availability_status" : false
    }
    ```
    Response for such request looks like:
    ```
    {
      "availability_status": false, 
      "category_id": 4, 
      "description": "Grooming appliance", 
      "name": "trimmer", 
      "price": 1120, 
      "success": true
    }
    ```
    Permitted Users : Admin  
  * DELETE: http://127.0.0.1:5000/products/<product_id>  
    This end point is used to delete the mentioned product by the product_id in the databse. It does not take any http request  
    body. A response for such a request looks like:  
    ```
    {
      "id": 11, 
      "message": "Deleted Successfully"
    }
    ```
    Permitted Users : Admin  
  * GET: http://127.0.0.1:5000/users  
    This api end point is used to get all the registered users to the platform. A response to a request made to the api looks like:  
    ```
    {
      "success": true, 
      "users": [
        {
          "id": 4, 
          "name": "Hermione Granger"
        }, 
        {
          "id": 5, 
          "name": "Ron Weasley"
        }, 
        {
          "id": 6, 
          "name": "Harry Potter"
        }
      ]
    }
    ```
    Permitted Users : Admin  
  * POST: http://127.0.0.1:5000/users  
    This endpoint takes a JSON object of the new user about to get registered and adds the user to the database:  
    ```
    {
      "name" : "Aman Bhardwaj"
    }
    ```
    Response would look like after a successful registration:  
    ```
    {
      "message": "Successfully Inserted in the database", 
      "success": true, 
      "user_name": "Hermione Granger"
    }
    ```
    Permitted Users : Admin  
  * DELETE: http://127.0.0.1:5000/users/<user_id>  
    This end point is used to remove a user from the database. A response from such a request looks like:  
    ```
    {
      "id": 5, 
      "message": "Deleted Successfully"
    }
    ```
    Permitted Users : Admin  
  * POST: http://127.0.0.1:5000/purchase  
    This end point allows user to make a purchase of a product. Takes a JSON body which couples user_id and product_id:  
    ```
    {
      "user_id" : 4,
      "product_id" : 3
    }
    ```
    Successful response from such a request looks like:  
    ```
    {
      "message": "Thankyou for shopping with us!!", 
      "product_id": 6, 
      "success": true, 
      "user_id": 4
    }
    ```
    Permitted Users : Customer   
  * GET: http://127.0.0.1:5000/transactions  
    This endpoint is used to get all the transactions happed against a user. A response when a request made to the api looks like:    
    ```
    {
      "success": true, 
      "userproducts": [
        {
          "product": 3, 
          "user": 6
        }, 
        {
          "product": 3, 
          "user": 4
        }, 
        {
          "product": 6, 
          "user": 6
        }
      ]
    }
    ```
    Permitted Users : Admin  

## Error responses:  
  * 400 Bad Request : As the name suggests something is not proper with the request body or the request argument.  
    For example, missing a required key in the request body JSON object. Example of how the response looks:  
    ```
    {
        "success": False, 
        "error": 400,
        "message": "Bad request"
    }
    ```
  * 404 Not Found : The requested resource is not present in the database. For example, when the id of the question  
    that needs to be deleted is not present in the database. Example of how the response looks:  
    ```
    {
        "success": False, 
        "error": 404,
        "message": "Resource not found"
    }
    ```
  * 422 Unprocessable : When everything is fine with the request and the resource is also present in the DB, but somehow  
    the action cannot be performed on the database, or something cannot be processed. Example of how the response looks:    
    ```
    {
        "success": False, 
        "error": 422,
        "message": "Unprocessable"
    }
    ```
  * 405 Method not allowed : When a resource is accessed with the wrong HTTP method. Example:    
    ```
    {
        "success": False, 
        "error": 405,
        "message": "Method not allowed"
    }
    ```
  * 403 Forbidden: When a request is made with missing permissions:  
    ```
    {
        "success": False, 
        "error": 403,
        "message": "Forbidden from accessing the resource"
    }
    ```
  * 401 Unauthorized: When a request is made from an unauthorized user:  
    ```
    {
        "success": False, 
        "error": 401,
        "message": "Unauthorized"
    }
    ```
## Important Notes:  
  * All the APIs must be called with proper JWT bearer token in the authorization header.
  * Currently, the project does not have a complete user registration flow. And it is assumed that the users  
    will currently be entered using the admin JWT token
