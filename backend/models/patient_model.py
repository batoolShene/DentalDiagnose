from sqlalchemy import Column, Integer, String, Date
from database import db  # adjust if your db import is different

class Patient(db.Model):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    birthdate = Column(Date, nullable=False)
    gender = Column(String(10), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<Patient(id={self.id}, name={self.name}, birthdate={self.birthdate})>"
