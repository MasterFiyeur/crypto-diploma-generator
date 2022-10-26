import jwt # JSON Web Tokens https://pyjwt.readthedocs.io/en/stable/usage.html#encoding-decoding-tokens-with-hs256
from functools import wraps # Decorator
from flask import request, redirect # API framework
from etc.settings import CONFIG # Settings


# Decorator to check if the user is authenticated
def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
        token = request.cookies.get('auth_token')
        if token is None:
            resp = redirect('/', 303)
            resp.set_cookie('auth_token', '', expires=0)
        try:
            data = jwt.decode(token, CONFIG['JWT_SECRET_KEY'], algorithms=["HS256"])
        except:
            resp = redirect('/', 303)
            resp.set_cookie('auth_token', '', expires=0)
            return resp
        return f(*args, **kwargs)
   return decorator