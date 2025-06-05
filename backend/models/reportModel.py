from services.database.database_service import db_service # Import SQLAlchemy instance

class Report(db_service.Model):
    __tablename__ = 'reports'  # Your actual db_service table name

    id = db_service.Column(db_service.Integer, primary_key=True)
    patient_name = db_service.Column(db_service.String(100), nullable=False)
    date = db_service.Column(db_service.Date, nullable=False)
    report_type = db_service.Column(db_service.String(50), nullable=False)
    details = db_service.Column(db_service.Text, nullable=True)

    def __repr__(self):
        return f"<Report {self.id} - {self.patient_name}>"
