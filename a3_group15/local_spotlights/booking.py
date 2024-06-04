from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Order,
from .forms import TicketBookingForm
from flask_login import login_required, current_user
from . import db

eventbp = Blueprint('event', __name__, url_prefix='/events')

# Book event ticket
@eventbp.route('/booking', methods = ['GET', 'POST'])
@login_required

def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    form = TicketBookingForm()
    if not event:
        abort(404)
    return render_template('events/booking.html', event=event, form=form)


def booking(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    booking_form = TicketBookingForm()
    if booking_form.validate_on_submit():
            order = Order(
            ticket_type = booking_form.ticket_type.data,
            ticket_quantity = booking_form.quantity.data,
            user_id = current_user,
            event = event, 
            )
        #add the object to the database session 
        db.session.add(order)
        db.session.commit()
        flash('Succesfully created new event', 'success')
        return redirect(url_for('mail.booked_events'))


