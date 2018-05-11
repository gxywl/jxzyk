# _*_ encoding: utf-8 _*_
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), unique=True, index=True)
    pin = db.Column(db.String(64))
    username = db.Column(db.String(64))
    isadm = db.Column(db.Boolean, default=False)

    jxsources = db.relationship('Jxsource', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

    def verify_pin(self, pin):
        return self.pin == pin

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


class Zytype(db.Model):
    __tablename__ = 'zytypes'
    id = db.Column(db.Integer, primary_key=True)
    typename = db.Column(db.String(64))

    jxsources = db.relationship('Jxsource', backref='zytype', lazy='dynamic')

    def __repr__(self):
        return '<Zytype %r>' % self.typename


class Jxsource(db.Model):
    __tablename__ = 'jxsources'
    id = db.Column(db.Integer, primary_key=True)
    zyname = db.Column(db.String(64))
    filename = db.Column(db.String(64))
    uptime = db.Column(db.DateTime(), default=datetime.utcnow)
    countd = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    zytype_id = db.Column(db.Integer, db.ForeignKey('zytypes.id'))

    def __repr__(self):
        return '<Jxsource %r>' % self.id
