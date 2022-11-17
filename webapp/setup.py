from flask import Flask, render_template, jsonify, request, make_response, redirect # API framework
from marshmallow import Schema, fields, ValidationError # API validation
import os # Environment variables
import datetime as dt # Date and time management library
import jwt # JSON Web Tokens
import uuid
from includes.decorator import token_required # Decorator
from etc.settings import CONFIG # Settings
from includes.mailer import send_mail # Mailer
from includes.totp import totp
from includes.steganography import hide_data_in_png, recover_data_from_png, verify_ts

app = Flask(__name__)


@app.route('/login', methods=['GET'])
def login_page():
    if ( request.cookies.get('auth_token')):
        return redirect('/One-Time-Password', 302)
    return render_template('login.html')

@app.route('/One-Time-Password', methods=['GET'])
@token_required
def OTP_page(user):
    return render_template('OTP.html')


# Authentication token needed
@app.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')



# Parameters validation for login()
class LoginSchema(Schema):
    email = fields.Email(required=True)
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
        # Generate token and set it as a cookiehours
        token = jwt.encode(
            {
                'email' : 'test@test.test', 
                'exp' : dt.datetime.utcnow() + dt.timedelta(hours=int(CONFIG['JWT_EXPIRES_HOURS']))
            },
            CONFIG['JWT_SECRET_KEY'], 
            'HS256'
        )
        # TODO : Generate random key for OTP and put it in database
        resp = make_response(jsonify({'message': 'success', 'token': token}), 200)
        resp.set_cookie('auth_token', token, path='/')
        return resp
    else:
        return jsonify({'message': 'Invalid email/password'}), 401


@app.route('/api/key', methods=['GET'])
@token_required
def get_key(user):
    # Return the key associated to the user
    return jsonify({'key': CONFIG['OTP_KEY']})


class CreateSchema(Schema):
    firstName = fields.String(required=True)
    lastName = fields.String(required=True)
    email = fields.Email(required=True)
    certificateName = fields.String(required=True)
    OTP = fields.String(required=True)

@app.route('/api/create', methods=['POST'])
def create_diploma():
    # Validate parameters
    schema = CreateSchema()
    try:
        validated_data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if validated_data['OTP'] == totp(CONFIG['OTP_KEY']):
        # Create string to hide
        fileName = str(uuid.uuid4())
        hide_data_in_png(fileName, validated_data['firstName'], validated_data['lastName'], validated_data['certificateName'])
        # TODO : Create QR code with our signature
        send_mail(fileName, validated_data['email'])
        return jsonify({'message': 'success'}), 200
    else :
        return jsonify({'message': 'Invalid OTP'}), 403

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() == 'png'

@app.route('/api/verify', methods=['POST'])
def verify_diploma():
    # User input validation
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if not file or not allowed_file(file.filename):
        return jsonify({'message': 'Invalid file'}), 400

    # Verify the diploma
    fileName = str(uuid.uuid4())
    file.save(os.path.join('tmp', fileName + '.png'))
    firstName, lastName, diploma = recover_data_from_png(fileName)
    ts_verify, timestamp = verify_ts(fileName)
    # TODO : Verify QR code with our signature
    return jsonify({
        'user': {
            'firstName': firstName,
            'lastName': lastName,
            'certitifacteName': diploma,
            'timestamp': timestamp
        },
        'tsSignature': ts_verify,
        'qrSignature': True
    }), 200
    

# Flask run
if __name__ == "__main__":
    if not os.path.exists('webapp/etc/settings.py'):
        app.logger.critical('Please create a webapp/etc/settings.py file like the settings_example.py file')
        exit(1)
    app.run(debug=True ,host='127.0.0.1', port=5000)