from flask import Flask, render_template, jsonify, request, make_response # API framework
from marshmallow import Schema, fields, ValidationError # API validation
import os # Environment variables
import datetime as dt # Date and time management library
import jwt # JSON Web Tokens
from includes.decorator import token_required # Decorator


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Authentication token needed
@app.route('/home', methods=['GET'])
@token_required
def home():
    return "Homepage!"


# Parameters validation for login()
class LoginSchema(Schema):
    email = fields.Email()
    password = fields.String(required=True)


@app.route('/api/login', methods=['POST'])
def login():
    # Validate parameters
    schema = LoginSchema()
    try:
        validated_data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    # Check user/password combination
    if validated_data['email'].lower() == 'test@test.test' and validated_data['password'] == 'test':
        # Generate token and set it as a cookie
        token = jwt.encode(
            {
                'email' : 'test@test.test', 
                'exp' : dt.datetime.utcnow() + dt.timedelta(hours=int(os.getenv('JWT_EXPIRES_HOURS')))
            }, 
            os.getenv('JWT_SECRET_KEY'), 
            'HS256'
        )
        resp = make_response(jsonify({'message': 'success', 'token': token.decode('UTF-8')}), 200)
        resp.set_cookie('auth_token', token, path='/')
        return resp
    else:
        return jsonify({'message': 'Invalid email/password'}), 401


# Flask run
if __name__ == "__main__":
    if not os.path.exists('.env'):
        app.logger.critical('Please create a .env file like the .env.example file')
        exit(1)
    app.run(debug=True ,host='127.0.0.1', port=5000, load_dotenv=True)