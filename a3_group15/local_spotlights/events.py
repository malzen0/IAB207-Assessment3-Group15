from multiprocessing import Value
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, EventStatus, Comment, Order
from .forms import EventForm, CommentForm, TicketBookingForm, EditEventForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime, date, time, timedelta
from sqlalchemy import or_

eventbp = Blueprint('event', __name__, url_prefix='/events', static_folder='static')

# Filter functions
@eventbp.route('/')
def index():
    update_db()
    genres = request.args.getlist('genres')
    location = request.args.get('location','')
    date = request.args.get('date','')
    
    query = db.session.query(Event).join(EventStatus).filter(EventStatus.status != 'Inactive')

    if genres:
        query=query.filter(Event.genre.in_(genres))
        
    if location:
        location_filter = f"%{location}%"
        query = query.filter(
            or_(Event.venue.ilike(location_filter)))

    if date:
        try: 
            date_actual = datetime.strptime(date, '%Y-%m-%d')
            date_range_start = date_actual - timedelta(days=30)
            date_range_end = date_actual + timedelta(days=30)
            query = query.filter(Event.date.between(date_range_start,date_range_end))
            ## Exception handling
        except ValueError:
            pass
    
    events= query.all()
        
    return render_template('index.html', events=events, selected_genres=genres, location = location, date=date)

def update_db():
    current_date = date.today()

    events = db.session.query(Event).all()

    for event in events:
        event_status = db.session.query(EventStatus).filter_by(event_id=event.id).first()
        status_text = event_status.status if event_status else None
        if event.date < current_date and status_text == 'Open':
                db.session.query(EventStatus).filter_by(event_id=event.id).update({'status': 'Inactive'})
                db.session.commit()

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
            user_id = current_user.id,
            )
        
        #add the object to the database session 
        db.session.add(event)
        db.session.commit()
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

# My events - events created by current user
@eventbp.route('/my-events')
def my_events():
    user_events = db.session.query(Event).join(EventStatus).filter(Event.user_id == current_user.id).all()
    upcoming_events = [event for event in user_events if event.status.status == 'Open' or event.status.status == 'Sold Out' ]
    past_events = [event for event in user_events if event.status.status == 'Cancelled' or event.status.status == 'Inactive']
    return render_template('events/my_events.html', upcoming_events=upcoming_events, past_events=past_events)


@eventbp.route('/<id>/edit-event', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if not event:
        abort(404)

    if event.user_id != current_user.id:
        flash('You are not authorized to edit this event', 'danger')
        return redirect(url_for('eventbp.my_events'))
    
    form = EditEventForm(obj=event)
    if form.validate_on_submit():
        #Cannot reduce the number of tickets
        if form.ticket_quantity.data < event.ticket_quantity:
            flash('Ticket quantity cannot be less than the current ticket quantity.', 'danger')
        else:
            #Calculate the number of addtional tickets added
            quantity_change = form.ticket_quantity.data - event.ticket_quantity
            if quantity_change > 0:
                event.status.status = 'Open'

            #Update event details
            event.artist = form.artist.data
            event.genre = form.genre.data
            event.venue = form.venue.data
            event.start_time = form.start_time.data
            event.end_time = form.end_time.data
            event.date = form.date.data
            event.ticket_quantity = form.ticket_quantity.data
            event.ticket_price = form.ticket_price.data
            event.description = form.description.data
            
            # Update tickets_available in EventStatus
            event.status.tickets_available += quantity_change

            db.session.commit()
            flash('Event has been updated', 'success')
            return redirect(url_for('event.my_events'))
    
    return render_template('events/edit_event.html', form=form, event=event)

# Cancel the event
@eventbp.route('/<id>/cancel', methods = ['GET', 'POST'])
def cancel_event(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if not event:
        abort(404)

    if event.user_id != current_user.id:
        flash('You are not authorized to cancel this event', 'danger')
        return redirect(url_for('event.my_events'))

    event.status.status = 'Cancelled'
    db.session.commit()
    flash(f'Event for "{event.artist}" has been cancelled', 'success')
    return redirect(url_for('event.my_events'))

# Booked events 
@eventbp.route('/booked-events')
def booked_events():
    orders = db.session.query(Order).join(Event).join(EventStatus).filter(Order.user_id == current_user.id).all()
    upcoming_events = [(order, order.event) for order in orders if order.event.status.status == 'Open' or order.event.status.status == 'Sold Out']
    past_events = [(order, order.event) for order in orders if order.event.status.status == 'Cancelled' or order.event.status.status == 'Inactive']
    return render_template('events/booked_events.html', upcoming_events=upcoming_events, past_events=past_events)


# Book event ticket
@eventbp.route('/<id>/booking', methods = ['GET', 'POST'])
@login_required
def booking(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if not event:
        abort(404)

    event_status = db.session.scalar(db.select(EventStatus).where(EventStatus.event_id == id))
    if not event_status:
        abort(404)

    form = TicketBookingForm(event_id=id)
    if form.validate_on_submit():
        if form.ticket_quantity.data > event_status.tickets_available:
            flash('The number of tickets requested exceeds the available tickets.', 'danger')
        else:
            order = Order(ticket_quantity = form.ticket_quantity.data, event=event, user=current_user)
            #add the object to the database session 
            event_status.tickets_available -= form.ticket_quantity.data
            if event_status.tickets_available == 0:
                event_status.status= "Sold Out"
            db.session.add(order)
            db.session.commit()
            flash('Succesfully purchased tickets', 'success')
            return redirect(url_for('event.booked_events'))
    return render_template('events/booking.html', form=form, event=event)