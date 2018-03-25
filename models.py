from main import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    name = db.Column(db.String(30))
    skills = db.Column(db.String(300))
    posts = db.relationship('Post',backref='user', lazy=True)
    comments = db.relationship('Comment',backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.name = ''

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(80))
    content = db.Column(db.String(500))
    comments = db.relationship('Comment',backref='post', lazy=True)

    def __init__(self, user_id, title, content):
        self.user_id = user_id
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Post %r>' % self.title

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    content = db.Column(db.String(500))

    def __init__(self, user_id, post_id, content):
        self.user_id = user_id
        self.post_id = post_id
        self.content = content

    def __repr__(self):
        return '<Comment %r>' % self.content
