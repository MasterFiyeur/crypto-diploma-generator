from flask import Flask, render_template, jsonify, request, make_response, redirect # API framework
from marshmallow import Schema, fields, ValidationError # API validation
import os # Environment variables
import datetime as dt # Date and time management library
import jwt # JSON Web Tokens
from includes.decorator import token_required # Decorator
from flask_mail import Mail, Message
from etc.settings import CONFIG # Settings
from includes.totp import totp



app = Flask(__name__)
app.config.update(CONFIG['SMTP_CONFIG'])

mail = Mail(app)


@app.route('/mail', methods=['GET'])
def send_mail():
    try:
        msg = Message('Hello', sender = CONFIG['SMTP_CONFIG']['MAIL_USERNAME'], recipients = ['catherine.dicki98@ethereal.email'])
        msg.body = "Hello Flask message sent from Flask-Mail"
        app.logger.debug('Sending mail...')
        mail.send(msg)
        app.logger.debug('mail sended')
    except Exception as e:
        raise e
    return "Check Your Inbox !!!"


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
    return jsonify({'key': "KRUGS4ZANFZSAYJAONSWG4TFOQQGWZLZ"})

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': totp("KRUGS4ZANFZSAYJAONSWG4TFOQQGWZLZ")})

# Flask run
if __name__ == "__main__":
    if not os.path.exists('webapp/etc/settings.py'):
        app.logger.critical('Please create a webapp/etc/settings.py file like the settings_example.py file')
        exit(1)
    app.run(debug=True ,host='127.0.0.1', port=5000)