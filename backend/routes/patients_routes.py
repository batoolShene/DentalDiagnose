from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.patient_model import Patient  # keep this at top-level

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/api/patients/find', methods=['GET'])
@jwt_required()
def find_patient_by_name_and_birthdate():
    # Import db here to avoid circular import
    from app import db  

    name = request.args.get('name')
    birthdate = request.args.get('birthdate')  # expected as string: "YYYY-MM-DD"

    if not name or not birthdate:
        return jsonify({'message': 'Missing name or birthdate'}), 400

    try:
        patient = Patient.query.filter_by(name=name, birthdate=birthdate).first()

        if patient:
            return jsonify({
                'id': patient.id,
                'name': patient.name,
                'birthdate': str(patient.birthdate),
                'email': patient.email
            }), 200
        else:
            return jsonify({'message': 'Patient not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
