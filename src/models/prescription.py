# Import our db module
from datetime import datetime
from src.database import db
class Prescription(db.Model):
    """Class that represent a prescription

    Args:
        db (_type_): The superclass

    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70),nullable=False)
    body = db.Column(db.Text, nullable=False)
    expedition_date = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __repr__(self) -> str:
        """ Returns a representative string of the class            

        Returns:
            str: A representative string of the class
        """
        return 'Prescription>>> {self._title}'
    