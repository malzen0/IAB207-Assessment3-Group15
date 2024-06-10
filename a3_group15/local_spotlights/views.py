from datetime import date
from flask import Blueprint, render_template
from .models import Event, EventStatus
from .models import Event
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    update_db()
    # Query for events that are not inactive
    events = db.session.query(Event).join(EventStatus).filter(EventStatus.status != 'Inactive').all()
    return render_template('index.html', events=events)

# Update database for inactive event status
def update_db():
    current_date = date.today()
    events = db.session.query(Event).all()
    
    # Get status for each event
    for event in events:
        event_status = db.session.query(EventStatus).filter_by(event_id=event.id).first()
        status_text = event_status.status if event_status else None
        
        # If event date is in past and event status is open then update to inactive
        if event.date < current_date and status_text == 'Open':
                db.session.query(EventStatus).filter_by(event_id=event.id).update({'status': 'Inactive'})
                db.session.commit()