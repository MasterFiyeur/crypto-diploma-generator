from flask import Flask, render_template, jsonify, request, make_response # API framework
from marshmallow import Schema, fields, ValidationError # API validation
from dotenv import load_dotenv # Environment variables

from includes.decorator import token_required # Decorator


app = Flask(__name__)
load_dotenv('../.env')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/home', methods=['GET'])
@token_required
def home():
    return "Homepage!"


class LoginSchema(Schema):
    email = fields.Email()
    password = fields.String(required=True)


@app.route('/api/login', methods=['POST'])
def login():
    schema = LoginSchema()
    try:
        validated_data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    if validated_data['email'].lower() == 'test@test.test' and validated_data['password'] == 'test':
        token = 'test'
        resp = make_response(jsonify({'message': 'success'}))
        resp.set_cookie('auth_token', token, path='/')
        return resp
    else:
        return jsonify({'message': 'Invalid email/password'}), 401