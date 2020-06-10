import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, Boolean
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate

database_path = os.environ.get('DATABASE_URL', None)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  products = db.relationship('Product', backref='categories', lazy=True, cascade='delete, all' )

  def __init__(self, name):
    self.name = name

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    print("Before DELETE self")
    db.session.delete(self)
    print("Before commit")
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name
    }

'''
Product

'''
class Product(db.Model):  
  __tablename__ = 'products'

  id = Column(Integer, primary_key=True)
  category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
  name = Column(String)
  price = Column(Integer)
  availability_status = Column(Boolean)
  description = Column(String)
  userproducts = db.relationship('UserProduct', backref='products', lazy=True, cascade='delete, all' )

  def __init__(self, category_id, name, price, availability_status, description):
    self.category_id = category_id
    self.name = name
    self.price = price
    self.availability_status = availability_status
    self.description = description

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'category_id': self.category_id,
      'name': self.name,
      'description': self.description,
      'price' : self.price,
      'availability_status' : self.availability_status
    }
'''
User
'''
class User(db.Model):  
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  userproducts = db.relationship('UserProduct', backref='users', lazy=True, cascade='delete, all' )

  def __init__(self, name):
    self.name = name

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name
    }
class UserProduct(db.Model):  
  __tablename__ = 'userproducts'

  user_id = Column(Integer, ForeignKey('users.id'), primary_key=True ,nullable=False)
  product_id = Column(Integer, ForeignKey('products.id'), primary_key=True ,nullable=False)

  def __init__(self, product_id, user_id):
    self.product_id = product_id
    self.user_id = user_id

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'user': self.user_id,
      'product': self.product_id
    }



