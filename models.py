from main import db

association_table = db.Table('association', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('hackathon_id', db.Integer, db.ForeignKey('hackathon.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    name = db.Column(db.String(40))
    skills = db.Column(db.String(300))
    posts = db.relationship('Post', backref='user', lazy=True)
    hackathons = db.relationship('Hackathon', secondary=association_table, backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.name = ''

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, db.ForeignKey('user.name'))
    likes = db.Column(db.Integer)
    hackathon_id = db.Column(db.Integer, db.ForeignKey('hackathon.id'))
    idea = db.Column(db.String(500))
    commentlist = db.relationship('Comment', backref='post.id', lazy=True)

    def __init__(self, name, hackathon_id, content):
        self.name = name
        self.hackathon_id = hackathon_id
        self.idea = content
        self.likes = 0
        self.commentlist = []

    def __repr__(self):
        ret = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        ret['commentlist'] = self.commentlist
        return str(ret)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.name'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    message = db.Column(db.String(500))

    def __init__(self, user, post_id, content):
        self.user= user
        self.post_id = post_id
        self.message = content

    def __repr__(self):
        return str({user:self.user, message:self.message})

class Hackathon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    posts = db.relationship('Post', backref='hackathon', lazy=True)
    users = db.relationship('User', secondary=association_table, backref='hackathon', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Hackathon %s>' % self.name
