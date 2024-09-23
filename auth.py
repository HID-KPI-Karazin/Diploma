from flask import Flask, request, redirect
import requests
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

with open('config.json', 'r') as f:
    config = json.load(f)

CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
REDIRECT_URI = config['redirect_uri']

@app.route('/')
def home():
    return 'Welcome to ClickUp/CBR Integration! <a href="/login">Login with ClickUp</a>'

@app.route('/login')
def login():
    return redirect(f'https://app.clickup.com/api?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}')

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://app.clickup.com/api/v2/oauth/token'
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(token_url, json=payload)
    response_data = response.json()
    access_token = response_data['access_token']
    with open('access_token.txt', 'w') as token_file:
        token_file.write(access_token)
    return 'Authorization successful! You can now use the API. The access token has been stored.'

if __name__ == '__main__':
    app.run(debug=True)

