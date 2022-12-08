from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from secrets import token_hex

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    apitoken = db.Column(db.String, default=None, nullable=True)
    diary = db.relationship('Nutrition',secondary = 'diary',backref = 'author',lazy='dynamic')

    def __init__(self, first_name, last_name, username, email, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.apitoken = token_hex(16)

    def to_dict(self):
        return{
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'token': self.apitoken
        }

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def saveChanges(self):
        db.session.commit()

    def addToDiary(self, nutrition):
        self.diary.append(nutrition)
        db.session.commit()

    def removeFromDiary(self, nutrition):
        self.diary.remove(nutrition)
        db.session.commit()

class Nutrition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(150), nullable=False)
    serving_size = db.Column(db.Numeric(10,2))
    calories = db.Column(db.Numeric(10,2))
    protein = db.Column(db.Numeric(10,2))
    carbs = db.Column(db.Numeric(10,2))
    fat = db.Column(db.Numeric(10,2))

    def __init__(self, food_name, serving_size, calories, protein, carbs, fat):
        self.food_name = food_name
        self.serving_size = serving_size
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat

    def to_dict(self):
        return {
            'id': self.id,
            'food_name': self.food_name,
            'quantity': self.serving_size,
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat
        }
    
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nutrition_id = db.Column(db.Integer, db.ForeignKey('nutrition.id'), nullable=False)

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()