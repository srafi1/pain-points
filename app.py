from flask import Flask, render_template, session, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'whomst gonn guess this?'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)
from models import *
db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    if session.get('user'):
        name = User.query.filter_by(username=session['user']).first().name
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
        new_user = User(user, password1)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = user
    return redirect('/')

@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        name = request.form.get('name')
        skills = request.form.get('skills')
        valid = True
        if name == '':
            flash('Fill out your name')
            valid = False
        if valid:
            u = User.query.filter_by(username=session['user']).first()
            u.name = name
            u.skills = skills
            db.session.add(u)
            db.session.commit()
            return redirect('/')
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
    if session.get('user'):
        session.pop('user')
    if session.get('hackathon'):
        session.pop('hackathon')
    return redirect('/')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        hackathon_name = request.form.get('hackathon')
        if hackathon_name:
            h = Hackathon(hackathon_name)
            db.session.add(h)
            db.session.commit()
    hackathon = session.get('hackathon')
    if hackathon:
        return redirect('/feed')
    hackathons = Hackathon.query.filter_by().all()
    return render_template('choose_hackathon.html', hackathons=hackathons)

@app.route('/sign_in/<int:hackathon_id>')
def sign_in(hackathon_id):
    session['hackathon'] = hackathon_id
    return redirect('/feed')

@app.route('/sign_out')
def sign_out():
    session.pop('hackathon')
    return redirect('/home')

@app.route('/feed')
def feed():
    posts= [
        {
            'name': "Shaina",
            'likes': 0,
            'id':0,
            'idea': "Ad ea velit deserunt irure esse minim proident ut adipisicing irure ex adipisicing consectetur et ipsum labore deserunt. Est anim enim amet cupidatat ad consequat irure ad do consectetur quis dolor nostrud est qui. Tempor amet sint culpa et culpa duis sint esse laborum duis eiusmod. Esse enim proident enim eu aliquip do ea anim culpa tempor. Qui exercitation quis fugiat enim amet mollit officia ullamco. Est sit cillum tempor sit excepteur irure anim ad occaecat.",
            'commentlist': [
                {'user': 'comm', 'message':'idk'},
                {'user': 'comm2', 'message':'idk as well'}
            ]
        },
        {
            'name': "Shakil",
            'likes': 0,
            'id':1,
            'idea': "thing2",
            'commentlist': [
                {'user': 'comm3', 'message':'idk and'},
                {'user': 'comm4', 'message':'idk or'}
            ]
        }
    ]

    posts = Post.query.all()
    posts = str(posts).replace("u'", "'")

    return render_template('feed.html', posts=posts)

@app.route('/forum')
def forum():
    return render_template('forum.html')

@app.route('/network')
def network():
    return render_template('network.html')

@app.route('/user')
def user():
    u = session['user']
    user_info = {"id" : user.id, "username": user.username, "name": user.name, "skills" : user.skills}
    return jsonify({"user_info": user_info})

@app.route("/user/id/<int:user_id>")
def profile(user_id):
    u = User.query.filter_by(id = user_id).first()
    user_info = {"id" : user.id, "username": user.username, "name": user.name, "skills" : user.skills}
    return jsonify({"user_info": user_info})

@app.route("/user/posts")
def posts():
    user = session['user']
    posts_info = []
    for post in user.posts.all():
        post_info = {"id" : post.id, "title": post.title, "content": post.content}
        posts_info.append(post_info)
    return jsonify({"posts_info": posts_info})

@app.route("/user/id/<int:user_id>/posts")
def user_posts(user_id):
    user = User.query.filter_by(id = user_id).first()
    posts_info = []
    for post in user.posts.all():
        post_info = {"id" : post.id, "title": post.title, "content": post.content}
        posts_info.append(post_info)
    return jsonify({"posts_info": posts_info})

@app.route("/post/<int:post_id>/comments")
def comments(post_id):
    post = Post.query.filter_by(id = post_id).first()
    comments = []
    for comment in post.comments.all():
        comment_info = {"id": comment.id, "user_id": comment.user_id, "content":comment.content}
        comments.append(comment_info)
    return jsonify({"comments": comments})

@app.route("/new_post", methods=["POST"])
def new_post():
    content = request.form.get('content')
    post = Post(session['user'], session['hackathon'], content)
    db.session.add(post)
    db.session.commit()
    return redirect('/feed')

if __name__ == '__main__':
    app.run(debug=True)
