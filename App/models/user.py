from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=True)  
    competitions = db.relationship('UserCompetition', backref='user', lazy=True, cascade="all, delete-orphan")


    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


class Competition(db.Model):
    __tablename__ = 'competition'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(120), nullable=False)
    participants = db.relationship('UserCompetition', backref='competition', lazy=True, cascade="all, delete-orphan")

    def __init__(self, title, description, date):
        self.title = title
        self.description = description
        self.date = date


class UserCompetition(db.Model):
    __tablename__ = 'user_competition'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), primary_key=True)
    placement = db.Column(db.Integer)

