from app import db
from sqlalchemy.orm import relationship

from app import db

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_number = db.Column(db.String(20), nullable=False, unique=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    
    # Rename the backref to avoid naming conflict
    patient = db.relationship('Patient', backref='appointments', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'appointment_number': self.appointment_number,
            'patient_name': f'{self.patient.first_name} {self.patient.last_name}'
        }