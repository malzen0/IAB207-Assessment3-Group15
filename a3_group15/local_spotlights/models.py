from . import db
from datetime import datetime, date, time
from flask_login import UserMixin

# User Table
class User(db.Model, UserMixin):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email_id = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    mobile_num = db.Column(db.String(20))
    address = db.Column(db.String(100))
    
    comments = db.relationship('Comment', backref='user')
    events = db.relationship('Event', backref='user')
    order = db.relationship('Order', backref='user')
    
    # String print method 
    def __repr__(self):
        return f"Name: {self.name}"


# Event table 
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(80))
    description = db.Column(db.String(200))
    img = db.Column(db.String(400))
    genre = db.Column(db.String(100))
    venue = db.Column(db.String(300))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    ticket_quantity = db.Column(db.Integer)
    ticket_price = db.Column(db.Float(20))

    
    comments = db.relationship('Comment', backref='event')
    status = db.relationship('EventStatus', backref='event', uselist=False)
    order = db.relationship('Order', backref="event")
    
    # foreign keys 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    
    # String print method
    def __repr__(self):
        return f"Artist: {self.artist}"
    
                
#Event Status table 
class EventStatus(db.Model):
    __tablename__ = 'eventstatus'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20))
    tickets_available = db.Column(db.Integer)
    status_date = db.Column(db.DateTime, default = datetime.now())
    
    # Foriegn keys
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    #String print method
    def __repr__(self):
        return f"Status: {self.status}"
    
    
# Order table 
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
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