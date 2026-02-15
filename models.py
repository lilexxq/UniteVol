from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

# Create db instance here to avoid circular imports
db = SQLAlchemy()

class VolunteerProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    organisation = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('volunteer_project.id'), nullable=False)
    project = db.relationship('VolunteerProject')
