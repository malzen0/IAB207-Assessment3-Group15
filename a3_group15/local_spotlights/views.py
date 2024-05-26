from datetime import datetime
from flask import Blueprint, app, render_template, request, redirect, url_for
from sqlalchemy.orm import query
from .models import Event
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', events=events)

# filter events

#def filtered_events():
    
 #   genres = request.args.getlist('genres')
  #  location = request.args.get('location')
   # date = request.args.get('date')
    
#    request = Event.query
#    if genres:
#        request = query.filter(Event.genre.in_(genres))
#    if location: 
##        request = query.filter(Event.venue.contains(location))
 #   if date:
 #       try:
 #           date_obj = datetime.strptime(date, '%Y-%m-%d')
 #           request = query.filter(Event.date == date_obj)
  #      except ValueError:
   #         pass
        
 #   filtered_events = request.all()
  #  return render_template('index.html', events=filtered_events)
# Search 


