from . import db
from datetime import datetime
from flask_login import UserMixin

# User Table
class User(db.Model, UserMixin):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    # Password stores as hash value
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user')
    
    # String print method 
    def __repr__(self):
        return f"Name: {self.name}"


# Event table 
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    cost = db.Column(db.Float(20))
    
    comments = db.relationship('Comment', backref='event')
    
    # foreign keys 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('eventstatus.id'))
    
    # String print method
    def __repr__(self):
        return f"Name: {self.name}"
    
    
#Event Status table 
class EventStatus(db.Model):
    __tablename__ = 'eventstatus'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20))
    tickets_available = db.Column(db.Integer)
    
    
    #String print method
    def __repr__(self):
        return f"Status: {self.status}"
    
    
# Order table 
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    ticket_type = db.Column(db.String(200))
    ticket_quantity = db.Column(db.Integer)
    order_date = db.Column(db.DateTime, default=datetime.now())
    
    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    
    # String print method 
    def __repr__(self):
        return f"Order: {self.id}"


# Comment table 
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    
    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    
    # String print method 
    def __repr__(self):
        return f"Comment: {self.text}"