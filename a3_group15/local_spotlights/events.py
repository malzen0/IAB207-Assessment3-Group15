from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, EventStatus, Comment, Order
from .forms import EventForm, CommentForm, TicketBookingForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime, date, time

eventbp = Blueprint('event', __name__, url_prefix='/events', static_folder='static')

# Filter genres
@eventbp.route('/')
def index():
    genres = request.args.getlist('genres')
    current_date = date.today()
    base_query = db.session.query(Event, EventStatus.status).outerjoin(EventStatus, Event.id == EventStatus.event_id)

    if genres:
        base_query = base_query.filter(Event.genre.in_(genres))
    
    events = base_query.all()
    print("Initial event statuses: {events}")
                  
    for event in events:
        print("Checking event {event.id} - {event.artist} with date {event.date} and status {event.status}")    
        if event.date < current_date:
            print(f"Updating status for event {event.id} - {event.artist} to 'inactive'")
            db.session.query(EventStatus).filter_by(event_id=event.id).update({'status': 'inactive'})
            db.session.commit()
    events = base_query.all()

    return render_template('index.html', events=events, selected_genres=genres)

# Event 
@eventbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))        
    form = CommentForm()
    if not event:
        abort(404)  
    event_status = db.session.scalar(db.select(EventStatus).where(EventStatus.event_id == id))
    if not event_status:
        abort(404)
    
    return render_template('events/event_details.html', event=event, event_status=event_status, form=form) 

# Create event
@eventbp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = EventForm()
    if form.validate_on_submit():
        # Call function to check and return image 
        db_file_path = check_file_upload(form)
        event = Event(
            artist = form.artist.data,
            genre = form.genre.data,
            venue = form.venue.data,
            start_time = form.start_time.data,
            end_time = form.end_time.data,
            date = form.date.data,
            ticket_quantity = form.ticket_quantity.data,
            ticket_price = form.ticket_price.data,
            description = form.description.data, 
            img = db_file_path,
            )
        
        #add the object to the database session 
        db.session.add(event)
        flash('Succesfully created new event', 'success')
        
        #add event status
        event_status = EventStatus(event_id=event.id,status="Open",tickets_available=event.ticket_quantity)
        db.session.add(event_status)
        # commit to the database
        db.session.commit()

        # redirect if form is valid
        return redirect(url_for('main.index'))
    
    return render_template('events/create_event.html', form=form)

# File upload 
def check_file_upload(form):
    
    # get file data from form 
    fp = form.img.data
    filename = fp.filename
    
    # Get current path of module file and store image file relative to the path 
    BASE_PATH = os.path.dirname(__file__)
    
    # Upload the file location 
    upload_path = os.path.join(BASE_PATH, 'static/img', secure_filename(filename))
    db_upload_path = '/static/img/' + secure_filename(filename)
    
    # Save the file and return path 
    fp.save(upload_path)
    return db_upload_path

# Comments
@eventbp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()

    # Get the event object associated with the page and comment
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    
    if not event:
        abort(404)
    
    if form.validate_on_submit():
        
        # Read the comment from the form 
        comment = Comment(text=form.comment.data, event=event, user=current_user)
        db.session.add(comment)
        db.session.commit()
        
        # Flash success when comment uploads
        flash('Your comment has been added', 'success')
    return redirect(url_for('event.show', id = id))
            
# Cancel the event
@eventbp.route('/<id>/cancel')
def cancel(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    #
    # 
    # 
    return redirect(url_for('event.show', id=id))

# Booked events 
@eventbp.route('/booked-events')
def booked_events():
    orders = db.session.query(Order).filter_by(user_id=current_user.id).all()
    order_event_info = [(order, order.event) for order in orders]
    return render_template('events/booked_events.html', order_event_info=order_event_info)


# Book event ticket
@eventbp.route('/<id>/booking', methods = ['GET', 'POST'])
@login_required
def booking(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    print(event.artist)
    if not event:
        abort(404)

    event_status = db.session.scalar(db.select(EventStatus).where(EventStatus.event_id == id))
    print(event_status.status)
    if not event_status:
        abort(404)

    form = TicketBookingForm(event_id=id)
    if form.validate_on_submit():
        if form.ticket_quantity.data > event_status.tickets_available:
            flash('The number of tickets requested exceeds the available tickets.', 'danger')
        else:
            order = Order(ticket_quantity = form.ticket_quantity.data, event=event, user=current_user)
            #add the object to the database session 
            print(f'Before: {event_status.tickets_available}')
            event_status.tickets_available -= form.ticket_quantity.data
            if event_status.tickets_available == 0:
                event_status.status= "Sold Out"
            print(f'After: {event_status.tickets_available}')
            db.session.add(order)
            db.session.commit()
            flash('Succesfully purchased tickets', 'success')
            return redirect(url_for('event.booked_events'))
    return render_template('events/booking.html', form=form, event=event)