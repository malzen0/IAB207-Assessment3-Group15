from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import DateField, TimeField, IntegerField, SelectField, ValidationError 
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, FileField, IntegerField, FloatField, TelField 
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from .models import Event
from . import db
 
ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    mobile_num = TelField("Mobile Number", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")
    
class BookingButtonForm(FlaskForm):
    # This form only has a submit button which redirects to the booking page
    book_tickets = SubmitField("BOOK TICKETS HERE!")

class CommentForm(FlaskForm):
    comment = TextAreaField("Write a Comment", validators=[InputRequired()], render_kw={"class": "form-control custom-text-area"})
    submit = SubmitField("POST", render_kw={"class": "btn custom-btn"})

# This is the event creation form
class EventForm(FlaskForm):
    artist = StringField("Artist")
    genre = SelectField("Genre", choices=[('rock', 'Rock'), ('metal', 'Metal'), ('pop', 'Pop'), ('blues/jazz', 'Blues/Jazz'), ('country', 'Country'), ('alternative', 'Alternative')])
    venue = StringField("Venue")
    start_time = TimeField("Start Time")
    end_time = TimeField("End Time")
    date = DateField("Date")
    ticket_quantity = IntegerField("Ticket Quantity")
    ticket_price = FloatField("Ticket Price")
    description = TextAreaField("Description")
    img = FileField("Image", validators= [FileRequired(message='Image cannot be empty'), FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
    submit = SubmitField("Create Event")
    

#This is the ticket booking form 
class TicketBookingForm(FlaskForm):
    ticket_quantity = IntegerField("Ticket Quantity")
    submit = SubmitField("Book Ticket")
    
    
    