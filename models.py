from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from sqlalchemy import Text, LargeBinary
from sqlalchemy.orm import relationship

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    vcards = db.relationship('VCard', backref='owner', lazy=True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class VCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    
    full_name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(200), nullable=True)
    address = db.Column(db.Text, nullable=False)

    
    linkedin = db.Column(db.String(200), nullable=True)
    twitter = db.Column(db.String(200), nullable=True)
    instagram = db.Column(db.String(200), nullable=True)
    facebook = db.Column(db.String(200), nullable=True)

    
    about = db.Column(db.Text, nullable=True)
    services = db.Column(db.Text, nullable=True)

    
    monday = db.Column(db.String(50), nullable=True)
    tuesday = db.Column(db.String(50), nullable=True)
    wednesday = db.Column(db.String(50), nullable=True)
    thursday = db.Column(db.String(50), nullable=True)
    friday = db.Column(db.String(50), nullable=True)
    saturday = db.Column(db.String(50), nullable=True)
    sunday = db.Column(db.String(50), nullable=True)

    
    banner_image = db.Column(db.String(500), nullable=True)

    
    gallery_images = db.Column(db.Text, nullable=True)  

    
    
    description = db.Column(db.Text, nullable=True)
    testimonials = db.Column(db.Text, default='[]')
    
    profile_photo = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"VCard('{self.full_name}', '{self.company}', '{self.email}')"
