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

