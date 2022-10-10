import os # Environment variables
import jwt # JSON Web Tokens https://pyjwt.readthedocs.io/en/stable/usage.html#encoding-decoding-tokens-with-hs256
from functools import wraps # Decorator
from flask import jsonify, request, redirect, make_response # API framework


# Decorator to check if the user is authenticated
def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = request.cookies.get('auth_token')
       if not token:
           resp = make_response(redirect('/', 303, jsonify({'message': 'a valid token is missing'})))
           resp.set_cookie('auth_token', '', expires=0)
           return resp
       try:
           data = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])
       except:
           resp = redirect('/', 303, jsonify({'message': 'token is invalid'}))
           resp.set_cookie('auth_token', '', expires=0)
           return resp
       return f(*args, **kwargs)
   return decorator