from flask import Blueprint, jsonify
from services.database.database_service import db_service
import logging

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

@reports_bp.route('/', methods=['GET'])
def get_reports():
    try:
        query = """
            SELECT id, patient_id, doctor_id, report_file_path, created_at FROM reports

        """
        reports = db_service.execute_query(query, fetch=True)
        
        if reports is None:
            return jsonify({'error': 'Failed to fetch reports from database'}), 500
        
        # Convert date objects to ISO format strings
        for report in reports:
            if report.get('date') and hasattr(report['date'], 'isoformat'):
                report['date'] = report['date'].isoformat()
        
        return jsonify(reports), 200

    except Exception as e:
        logging.exception("Error fetching reports")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500
