from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Order
from .forms import TicketBookingForm
from flask_login import login_required, current_user
from . import db

ticketsbp = Blueprint('tickets', __name__,)


def get_ticket_quantity(event):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    return event.ticket_quantity

# Book event ticket
@ticketsbp.route('/booking/<id>', methods = ['GET', 'POST'])
@login_required
def booking(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if not event:
        abort(404)
    
    tickets_available = get_ticket_quantity(event)
    booking_form = TicketBookingForm()
    
    booking_form = TicketBookingForm()
    if booking_form.validate_on_submit():
        ticket_quantity = booking_form.quantity.data
        if ticket_quantity > tickets_available:
            flash('Not enough tickets available.', 'danger')
        else:
            order = Order(
            ticket_quantity = booking_form.quantity.data,
            user_id = current_user,
            event = event,)
        #add the object to the database session 
        db.session.add(order)
        event.ticket_quantity -= ticket_quantity
        db.session.commit()
        flash('Succesfully purchased tickets', 'success')
        return redirect(url_for('booking'))
    return render_template('booking.html', form=booking_form, id=id)
