# diploma-generator
Générateur de diplômes + stéganographie + envoie de mail

# To get testing SMTP server
Create an account [there](https://ethereal.email)

# Generate RSA private and public key
To generate private key : `openssl genrsa -out rsa.pem 2048` \
To generate public key from the private key : `openssl rsa -in rsa.pem -pubout > rsa.pub`

# To launch to project
Execute `python3 webapp/setup.py`