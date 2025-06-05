import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import config
from config.config import config

# Import the db instance (from database.py)
from database import db

# Import blueprints
from routes.auth_routes import auth_bp
from routes.process_routes import process_bp
from routes.detect_routes import detect_bp
from routes.admin_routes import admin_bp
from routes.dental_detection_route import dental_bp
from routes.register_routes import register_bp
from routes.reports_routes import reports_bp
from routes.patients_routes import patients_bp
from routes.images import image_bp  # Make sure this matches your file & variable name!

# Import services
from services.auth.auth_service import initialize_auth_system

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name='default'):
    app = Flask(__name__)

    # Load config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Setup DB config from env vars or config.py
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_name = os.getenv('DB_NAME', 'dental_diagnostic_system')
    db_port = os.getenv('DB_PORT', '3306')

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db with app
    db.init_app(app)

    # Create model directory if needed
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
    app.config['MODEL_DIR'] = model_dir
    os.makedirs(model_dir, exist_ok=True)

    # Enable CORS with credentials support
    CORS(app, supports_credentials=True)

    # Setup JWT
    JWTManager(app)

    # Initialize auth system
    try:
        logger.info("Initializing authentication system...")
        if not initialize_auth_system():
            logger.critical("Failed to initialize authentication system")
            raise RuntimeError("Database initialization failed")
        logger.info("Authentication system initialized successfully")
    except Exception as e:
        logger.exception("Error during app initialization")
        raise

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(process_bp, url_prefix='/api/process')
    app.register_blueprint(detect_bp, url_prefix='/api/detect')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(dental_bp, url_prefix='/api/dental')
    app.register_blueprint(register_bp, url_prefix='/api/register')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(image_bp)  # No prefix, uses route as defined in blueprint
    app.register_blueprint(patients_bp)

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'AIDentify API is running'}), 200

    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_CONFIG', 'default'))
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
