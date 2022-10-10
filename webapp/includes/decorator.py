import os # Environment variables
import jwt # JSON Web Tokens
import datetime as dt # Date and time management library
from functools import wraps # Decorator
from flask import jsonify, request, redirect # API framework

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = request.cookies.get('auth_token')
       print(token)
       if not token:
           return redirect('/', 303, jsonify({'message': 'a valid token is missing'}))
       try:
           data = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])
       except:
           return redirect('/', 303, jsonify({'message': 'token is invalid'}))
       return f(*args, **kwargs)
   return decorator