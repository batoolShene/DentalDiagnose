# backend/database.py
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

app = Flask(__name__)

# Load database URI from environment variables or construct it manually
db_user = os.getenv('DB_USER', 'root')
db_password = os.getenv('DB_PASSWORD', '')  # empty for XAMPP default
db_host = os.getenv('DB_HOST', 'localhost')
db_name = os.getenv('DB_NAME', 'dental_diagnostic_system')
db_port = os.getenv('DB_PORT', '3306')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
