from app import db
from datetime import datetime


class IgAccount(db.Model):
    __tablename__ = 'ig_account'
    # Constantes
    username = db.Column(db.String(64), primary_key=True)
    creation_date = db.Column(db.Date, default=datetime.utcnow().date)
    ig_datas = db.relationship('IgData', backref='datas', lazy='dynamic')
    def __repr__(self):
        return f'User : {self.username}'

class IgData(db.Model):
    __tablename__ = 'ig_data'
    id = db.Column(db.Integer, primary_key=True)
    # Variables
    update_date = db.Column(db.Date, default=datetime.utcnow().date)
    followers = db.Column(db.Integer)
    followings = db.Column(db.Integer)
    avg_likes = db.Column(db.Integer)
    avg_comments = db.Column(db.Integer)
    ig_account_username = db.Column(db.Integer, db.ForeignKey('ig_account.username'))

    def __repr__(self):
        return f'Date : {self.update_date}'