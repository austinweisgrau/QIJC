from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def sumpoints(self):
        sp = 0
        sp += 5 * len(self.subs)
        sp += 10 * len(self.vols)
        return sp

    def hotpoints(self):
        pass

class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    link = db.Column(db.String(140), unique=True)
    abstract = db.Column(db.String(512))
    subber_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    volunteer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    subber = db.relationship('User', backref='subs', foreign_keys=[subber_id])
    volunteer = db.relationship('User', backref='vols',
                             foreign_keys=[volunteer_id])
    
    def __repr__(self):
        return '<Post {}>'.format(self.title)
