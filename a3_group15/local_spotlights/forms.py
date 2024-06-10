from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import DateField, TimeField, IntegerField, SelectField, ValidationError 
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, FileField, IntegerField, FloatField, TelField 
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, Regexp
from .models import EventStatus
import datetime
 
ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    first_name=StringField("First Name", validators=[InputRequired()])
    last_name=StringField("Last Name", validators=[InputRequired()])
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
    
    # Event date validation - date cannot be in the past
    def validate_date(form, date):
        if date.data < datetime.date.today():
            raise ValidationError("The date cannot be in the past!")

#This is the ticket booking form 
class TicketBookingForm(FlaskForm):
    ticket_quantity = IntegerField("Ticket Quantity", validators=[InputRequired(), NumberRange(min = 1)])
    cardholder_name = StringField('Cardholder Name', validators=[InputRequired()])
    card_number = StringField('Card Number', validators=[InputRequired(), Length(min=16, max=19)])
    expiration_date = StringField('Expiration Date', validators=[InputRequired(), Regexp(r'^\d{2}/\d{2}$', message='MM/YY format')])
    cvv = StringField('CVV', validators=[InputRequired(), Length(min=3, max=4)])
    submit = SubmitField("Book Ticket")

#This is the edit event form
class EditEventForm(FlaskForm):
    artist = StringField('Artist', validators=[InputRequired()])
    genre = SelectField("Genre", choices=[('rock', 'Rock'), ('metal', 'Metal'), ('pop', 'Pop'), ('blues/jazz', 'Blues/Jazz'), ('country', 'Country'), ('alternative', 'Alternative')])
    venue = StringField('Venue', validators=[InputRequired()])
    start_time = TimeField('Start Time', validators=[InputRequired()])
    end_time = TimeField('End Time', validators=[InputRequired()])
    date = DateField('Date', validators=[InputRequired()])
    ticket_quantity = IntegerField('Ticket Quantity', validators=[InputRequired()])
    ticket_price = FloatField('Ticket Price', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    submit = SubmitField('Update Event')
    
    def validate_date(form, date):
        if date.data < datetime.date.today():
            raise ValidationError("The date cannot be in the past!")
