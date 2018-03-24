from flask import Flask, render_template, session, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'whomst gonn guess this?'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)
from models import *
db.create_all();

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    if session.get('user'):
        name = User.query.filter_by(username=session['user']).first().name 
        print name
        if name == '':
            return redirect('/create_profile')
        else:
            return redirect('/home')
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    user = request.form.get('username')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    valid = True
    if User.query.filter_by(username=user).count() > 0:
        flash('That username is taken')
        valid = False
    if password1 == '':
        flash('Password should not be empty')
        valid = False
    if password1 != password2:
        flash('Passwords should match')
        valid = False
    if user == '':
        flash('Username should not be empty')
        valid = False
    if valid:
        print 'creating user:', user, password1, password2
        new_user = User(user, password1)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = user
    else:
        print 'invalid register'
    return redirect('/')

@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        name = request.form.get('name')
        skills = request.form.get('skills')
        if name == '':
            flash('Fill out your name')
        if skills == '':
            flash('Fill out your skills')
    return render_template('create_profile.html')

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('username')
    password = request.form.get('password')
    u = User.query.filter_by(username=user, password=password).first()
    if u:
        session['user'] = user
    else:
        flash('Login failed')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

@app.route('/forum')
def forum():
    return render_template('forum.html')

@app.route('/network')
def netowrk():
    return render_template('network.html')

if __name__ == '__main__':
    app.run(debug=True)
