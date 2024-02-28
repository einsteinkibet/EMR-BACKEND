from flask import request, jsonify
from app import db
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.models.patients import Patient  # Import the Patient class from app.models.patients
from datetime import datetime, date, timedelta


logging.basicConfig(level=logging.INFO)


def handle_error(e, status_code):
    logging.error(str(e))
    return jsonify({'error': str(e)}), status_code


from datetime import datetime

def create_patient(first_name, last_name,age , gender, contact_number, address, description, location_input, summarized_descrition, date_served, served_by, medicine, disease, doctor):
    try:
        data = request.get_json()

        # Check for missing fields
        required_fields = ['first_name', 'last_name', 'age', 'gender', 'contact_number', 'address']
        if not all(field in data for field in required_fields):
            return handle_error('Missing required fields', 400)
        
        # Convert date_served string to datetime object with date only
        date_served_str = data.get('date_served', '')
        date_served = datetime.strptime(date_served_str, '%Y-%m-%d').date()
      
        # Create a new Patient object
        patient = Patient(
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            contact_number=contact_number,
            address=address,
            description=description,
            date_served=date_served,
            location_input=location_input,
            summarized_descrition=summarized_descrition,
            served_by=served_by,
            medicine=medicine,
            disease=disease,
            doctor=doctor)

        # Add the new patient to the database
        db.session.add(patient)
        db.session.commit()
        serialized_patient = patient.serialize()
        return jsonify(serialized_patient), 201

    except SQLAlchemyError as e:
        # Log the error
        logging.error(f"SQLAlchemyError: {str(e)}")

        # Rollback the session in case of error
        db.session.rollback()
        return handle_error(e, 500)


def get_patients():
    try:
        patients = Patient.query.all()
        return jsonify([patient.serialize() for patient in patients]), 200

    except SQLAlchemyError as e:
        return handle_error(e, 400)



def get_patient(id):
    """Get a specific patient by ID."""
    try:
        # Retrieve the patient from the database by ID
        patient = Patient.query.get(id)
        
        if patient:
            # If the patient exists, return the serialized patient data
            return jsonify(patient.serialize()), 200
        else:
            # If the patient does not exist, return a 404 Not Found response
            return jsonify({'message': 'Patient not found'}), 404
    except Exception as e:
        # If any error occurs, return a 500 Internal Server Error response
        return handle_error(e, 400)


def update_patient(id):
    try:
        patient = Patient.query.get(id)
        if not patient:
            return jsonify('Patient not found'), 404

        description = request.json.get('description', '')
        location_input = request.json.get('location_input', '')
        medicine = request.json.get('medicine', '')
        disease = request.json.get('disease', '')
        doctor = request.json.get('doctor', '')

        # Convert date_served string to a Python date object
        date_served_str = request.json.get('date_served')
        if date_served_str:
            date_served = datetime.strptime(date_served_str, '%Y-%m-%d').date()
        else:
            date_served = None

        # Update patient attributes
        patient.description = description
        patient.date_served = date_served
        patient.location_input = location_input
        patient.medicine = medicine
        patient.disease = disease
        patient.doctor = doctor

        db.session.commit()
        return jsonify('Patient updated successfully'), 200

    except SQLAlchemyError as e:
        return jsonify(str(e)), 400
def delete_patient(id):
    try:
        patient = Patient.query.get(id)
        db.session.delete(patient)
        db.session.commit()
        return jsonify("patient deleted successfully")
    except SQLAlchemyError as e:
        return handle_error(e, 400)
