from flask import request, jsonify
from app import db
from app.models.appointment import Appointment
from app.models.patients import Patient
from sqlalchemy.exc import SQLAlchemyError
import logging

logging.basicConfig(level=logging.INFO)

def handle_error(e, status_code):
    logging.error(f'Error: {str(e)}')
    return jsonify({'error': str(e)}), status_code


def create_appointment(data):
    try:
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        patient = Patient.query.filter_by(first_name=first_name, last_name=last_name).first()

        # Create a new appointment object
        appointment = Appointment(
            appointment_number =data['appointment_number'],
            patient =patient
        )
        # Add the appointment to the database
        db.session.add(appointment)
        db.session.commit()

        serialized_appointment = appointment.serialize()
        serialized_appointment['patient_name'] = f"{patient.first_name} {patient.last_name}"

        return jsonify(serialized_appointment), 201


    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: {str(e)}")
        db.session.rollback() 
        return handle_error(e, 500)


def get_appointments():
    try:
        appointments = Appointment.query.all()
        return jsonify([appointment.serialize() for appointment in appointments]), 200
    except SQLAlchemyError as e:
        return handle_error(e, 400)

def get_appointment(id):
    try:
        appointment = Appointment.query.filter_by(id=id).first()
        if appointment:
            return jsonify(appointment.serialize()), 200
        else:
            return jsonify({'error': 'Appointment not found'}), 404
    except SQLAlchemyError as e:
        return handle_error(e, 400)
# Add other controller functions as needed (e.g., update and delete)
