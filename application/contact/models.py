from datetime import datetime
from application import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    webpage = db.Column(db.String, nullable=False)
    submit_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Data('{self.webpage}', '{self.submit_time}', '{self.description}'"