from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from datetime import datetime, date



class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.String(20))
    gender = db.Column(db.String(100))
    contact_number = db.Column(db.String(250))
    address = db.Column(db.String(250))
    description = db.Column(db.String(250), nullable=True)
    date_served = db.Column(db.Date, default=date.today(), nullable=True)
    location_input = db.Column(db.String(250))
    summarized_descrition = db.Column(db.String(250), nullable=True)
    served_by = db.Column(db.String(250), nullable=True)
    medicine = db.Column(db.String(250), nullable=True)
    disease = db.Column(db.String(250), nullable=True)
    doctor = db.Column(db.String(250), nullable=True)
    # appointments = db.relationship('Appointment', backref='patient', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'gender': self.gender,
            'contact_number': self.contact_number,
            'address': self.address,
            'description': self.description,
            'date_served': self.date_served,
            'location_input': self.location_input,
            'summarized_descrition': self.summarized_descrition,
            'served_by': self.served_by,
            'medicine':self.medicine,
            'disease':self.disease,
            'doctor':self.doctor,

        }

