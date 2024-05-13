from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo
 
#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")
    
class BookingButtonForm(FlaskForm):
    # This form only has a submit button which redirects to the booking page
    book_tickets = SubmitField("BOOK TICKETS HERE!")

class CommentForm(FlaskForm):
    comment = TextAreaField("Write a Comment", validators=[InputRequired()])
    submit = SubmitField("POST")

# This is the event creation form
class EventForm(FlaskForm):
    artist = StringField("Artist")
    genre = SelectField("Genre", choices=[('rock', 'Rock'), ('metal', 'Metal'), ('pop', 'Pop'), ('blues/jazz', 'Blues/Jazz'), ('country', 'Country'), ('alternative', 'Alternative')])
    venue = StringField("Venue")
    time = StringField("Time")
    date = DateField("Date")
    ticket_quantity = StringField("Ticket Quantity")
    ticket_price = StringField("Ticket Price")
    comments = SelectField("Comments?", choices=[('yes', 'Yes'), ('no', 'No')])
    status = SelectField("Status", choices=[('open', 'Open'), ('inactive', 'Inactive'), ('sold out', 'Sold Out'), ('cancelled', 'Cancelled')])
    description = TextAreaField("Description")
    img = StringField("Image")
    submit = SubmitField("Create Event")

#This is the ticket booking form 
class TicketBookingForm(FlaskForm):
    full_name = StringField("Full Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    address = StringField("Address", validators=[InputRequired()])
    city = StringField("City", validators=[InputRequired()])
    state = StringField("State", validators=[InputRequired()])
    zip_code = StringField("Zip", validators=[InputRequired()])
    # Payment information
    payment_method = SelectField("Payment Method", choices=[('card', 'Credit/Debit Card'), ('paypal', 'PayPal')], validators=[InputRequired()])
    name_on_card = StringField("Name on Card")
    credit_card_number = StringField("Credit Card Number")
    expiration_month = SelectField("Expiration Month", choices=[('01', 'January'), ('02', 'February'), ..., ('12', 'December')], validators=[InputRequired()])
    expiration_year = SelectField("Expiration Year", choices=[('2022', '2022'), ('2023', '2023'), ..., ('2030', '2030')], validators=[InputRequired()])
    cvv = StringField("CVV")
    quantity = IntegerField("Quantity", validators=[InputRequired(), NumberRange(min=1, message="Please select at least 1 ticket")])
    submit = SubmitField("COMFIRM PAYMENT")

