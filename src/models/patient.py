# Import our db module
from src.database import db
from datetime import datetime
class Patient(db.Model):
    """Class that represents a Patient, inherets from Model

    Args:
        db (Model): The superclass 
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True, nullable=False)
    password = db.Column(db.Text(),unique=True, nullable=False)
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    address = db.Column(db.String(100))
    prescriptions = db.relationship('Prescription',backref="patient") 
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __repr__(self) -> str:
        """Returns a representative string of the class

        Returns:
            str: The representative string of the class with the username
        """
        return 'User>>>{self.username}'