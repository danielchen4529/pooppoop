from datetime import datetime
from app.models import db

class PoopLog(db.Model):
    """PoopLog Model representing individual poop records."""
    __tablename__ = 'poop_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    bristol_type = db.Column(db.Integer, db.CheckConstraint('bristol_type BETWEEN 1 AND 7'), nullable=False)
    color = db.Column(db.String(30), nullable=False)
    odor = db.Column(db.String(30), nullable=True)
    mood = db.Column(db.String(30), nullable=False)
    note = db.Column(db.Text, nullable=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- CRUD Static & Class Methods ---
    @classmethod
    def create(cls, bristol_type, color, mood, date_time, user_id=None, odor=None, note=None):
        """Create a new poop log and save to database."""
        log = cls(
            user_id=user_id,
            bristol_type=bristol_type,
            color=color,
            odor=odor,
            mood=mood,
            note=note,
            date_time=date_time
        )
        db.session.add(log)
        db.session.commit()
        return log

    @classmethod
    def get_by_id(cls, log_id):
        """Retrieve a poop log by its ID."""
        return cls.query.get(log_id)

    @classmethod
    def get_all(cls, user_id=None, start_date=None, end_date=None):
        """Retrieve all poop logs, optionally filtered by user and/or date range."""
        query = cls.query
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        if start_date:
            query = query.filter(cls.date_time >= start_date)
        if end_date:
            query = query.filter(cls.date_time <= end_date)
        
        # Default order is descending by the recorded poop date_time
        return query.order_by(cls.date_time.desc()).all()

    def update(self, bristol_type=None, color=None, odor=None, mood=None, note=None, date_time=None):
        """Update poop log fields."""
        if bristol_type is not None:
            self.bristol_type = bristol_type
        if color is not None:
            self.color = color
        if odor is not None:
            self.odor = odor
        if mood is not None:
            self.mood = mood
        if note is not None:
            self.note = note
        if date_time is not None:
            self.date_time = date_time
        
        # update the updated_at timestamp as well
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self

    def delete(self):
        """Delete the poop log from database."""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<PoopLog Type={self.bristol_type} Color={self.color} Mood={self.mood} User={self.user_id}>"
