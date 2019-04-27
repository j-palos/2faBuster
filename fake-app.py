from flask import (Flask, render_template, redirect, url_for, request)
app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return "I'M IN!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pswd = request.form['password']
        if user == 'pepe' and pswd == 'password':
            return redirect(url_for('twofa'))
        return render_template('twofabuster.html',
                               error="Invalid username or password.")

    return render_template('twofabuster.html')

@app.route('/2fa', methods=['GET', 'POST'])
def twofa():
    if request.method == 'POST':
        tok = request.form['token']
        if tok == '123456':
            return redirect(url_for('home'))
        return redirect(url_for('login'))

    return render_template('authtoken.html')
