from main import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    name = db.Column(db.String(30))
    skills = db.Column(db.String(300))
    posts = db.relationship('Posts',backref='user', lazy=True)
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.name = ''

    def __repr__(self):
        return '<User %r>' % self.username
