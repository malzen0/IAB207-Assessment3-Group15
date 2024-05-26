from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, EventStatus, Comment
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

eventbp = Blueprint('event', __name__, url_prefix='/events')

# Event 
@eventbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    form = CommentForm()
    if not event:
        abort(404)
    return render_template('events/event_details.html', event=event, form=form) 

# Create event
@eventbp.route('/create', methods = ['GET', 'POST'])
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
            date = form.date.data,
            ticket_quantity = form.ticket_quantity.data,
            ticket_price = form.ticket_price.data,
            description = form.description.data, 
            img = db_file_path)
        #add the object to the database session 
        db.session.add(event)
        # commit to the database
        db.session.commit()
        flash('Succesfully created new event', 'success')
        # redirect if form is valid
        return redirect(url_for('event.create'))
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

# login 
