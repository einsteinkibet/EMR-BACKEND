from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.controllers.user_controller import create_user, get_users, get_user, update_user, delete_user, get_user_by_username, login
from app.controllers.patients_controller import create_patient, get_patients, update_patient, delete_patient, get_patient
from app.models.user_model import User  # Add this import
from app.models.patients import Patient
from app.models.appointment import Appointment
from app.controllers.appointment_controller import create_appointment, get_appointments, get_appointment
from app import db  # Import 'create_app' and 'db' from __init__.py
from datetime import datetime

bp = Blueprint('bp', __name__)



@bp.route('/user', methods=['POST'])
def add_user_route():
    """Create a new user."""
    data = request.json
    username = data.get('username', '')
    role = data.get('role', '')

    # Check if the username already exists
    existing_user = get_user_by_username(username)
    if existing_user:
        return jsonify({'message': 'Error: Username already exists. Please choose another username.'}), 400

    # Check if the username length is valid
    if len(username) < 5:
        return jsonify({'message': 'Error: Username must be at least 5 characters.'}), 400

    # If username is unique and length is okay, proceed with user creation
    response, status_code = create_user()
    return jsonify(response), status_code


@bp.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin()  # Allow CORS for the /login route
def login_():
    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        return jsonify({'message': 'CORS preflight request handled'}), 200

    # Continue with your login logic
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    role = data.get('role')


    # Call your login function
    return login(username, password,role)
   
@bp.route('/user', methods=['GET'])
def get_users_route():
    """Get all users."""
    return get_users()

@bp.route('/user/<int:id>')
def get_user_route(id):
    """Get a specific user by ID."""
    return get_user(id)

@bp.route('/user/<int:id>', methods=['PUT', 'PATCH'])
def update_user_route(id):
    """Update a user by ID."""
    return update_user(id)

@bp.route('/user/<int:id>', methods=['DELETE'])
def delete_user_route(id):
    """Delete a user by ID."""
    return delete_user(id)




from flask import request, jsonify
from app import db
from app.models.patients import Patient
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

def handle_error(e, status_code):
    return jsonify({'error': str(e)}), status_code
@bp.route('/patient', methods=['POST'])
def create_patient():
    """Create a new patient."""
    try:
        data = request.json

        # Convert date_served string to datetime object with date only
        date_served_str = data.get('date_served', '')
        if date_served_str:
            date_served = datetime.strptime(date_served_str, '%Y-%m-%d').date()
        else:
            date_served = None

        new_patient = Patient(
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data['age'],
            gender=data['gender'],
            contact_number=data['contact_number'],
            address=data['address'],
            description=data['description'],
            date_served=date_served,  # Correctly converted to Python date object
            location_input=data['location_input'],
            summarized_descrition=data['summarized_descrition'],
            served_by=data['served_by'],
            medicine=data['medicine'],
            disease=data['disease'],
            doctor=data['doctor']
        )
        # Add the new patient to the database
        db.session.add(new_patient)
        db.session.commit()
        return jsonify(new_patient.serialize()), 201

    except Exception as e:
        db.session.rollback()
        return handle_error(e, 500)

@bp.route('/patient')
def get_patients_route():
    """Get all patients."""
    return get_patients()

@bp.route('/patient/<int:id>')
def get_patient_route(id):
    """Get a specific patient by ID."""
    return get_patient(id)

@bp.route('/patient/<int:id>', methods=['PUT', 'PATCH'])
def update_patient_route(id):
    """Update a patient by ID."""
    return update_patient(id)

@bp.route('/patient/<int:id>', methods=['DELETE'])
def delete_patient_route(id):
    """Delete a patient by ID."""
    return delete_patient(id)

@bp.route('/appointments', methods=['POST'])
def add_appointment_route():
    data = request.json
    response, status_code = create_appointment(data)
    return jsonify(response), status_code

# Add other routes as needed


# Route to fetch all appointments
# Route to fetch all appointments
@bp.route('/appointments', methods=['GET'])
def get_appointments_route():
    return get_appointments()

# Remove conflicting route
@bp.route('/appointment/<int:id>')
def get_appointment_route(id):
    """Get a specific appointment by ID."""
    return get_appointment(id)
