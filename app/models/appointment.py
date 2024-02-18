from app import db
from sqlalchemy.sql import func  # Import func from SQLAlchemy

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False, default=func.now())
    def __repr__(self):
        return f"Appointment(id={self.id}, doctor_id={self.doctor_id}, patient_id={self.patient_id}, appointment_date={self.appointment_date}, description={self.description})"
