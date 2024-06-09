from datetime import date
from flask import Blueprint, app, render_template, request, redirect, url_for
from .models import Event, EventStatus
from .models import Event
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    update_db()
    genres = request.args.getlist('genres')
    if not genres:
        events = db.session.query(Event).join(EventStatus).filter(EventStatus.status != 'Inactive').all()
    else:
        events = db.session.query(Event).join(EventStatus).filter(EventStatus.status != 'Inactive', Event.genre.in_(genres)).all()
    
    return render_template('index.html', events=events, selected_genres=genres)

def update_db():
    current_date = date.today()
    events = db.session.query(Event).all()
    for event in events:
        event_status = db.session.query(EventStatus).filter_by(event_id=event.id).first()
        status_text = event_status.status if event_status else None
        if event.date < current_date and status_text == 'Open':
                db.session.query(EventStatus).filter_by(event_id=event.id).update({'status': 'Inactive'})
                db.session.commit()