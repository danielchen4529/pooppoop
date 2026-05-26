from datetime import datetime
from app.models import db

class DietSuggestion(db.Model):
    """DietSuggestion Model representing system/AI generated health or dietary advice."""
    __tablename__ = 'diet_suggestions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    summary = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # --- CRUD Static & Class Methods ---
    @classmethod
    def create(cls, user_id, summary, content):
        """Create a new diet suggestion record and save to database."""
        suggestion = cls(user_id=user_id, summary=summary, content=content)
        db.session.add(suggestion)
        db.session.commit()
        return suggestion

    @classmethod
    def get_by_id(cls, suggestion_id):
        """Retrieve a diet suggestion by its ID."""
        return cls.query.get(suggestion_id)

    @classmethod
    def get_by_user_id(cls, user_id, limit=10):
        """Retrieve latest diet suggestions for a specific user."""
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).limit(limit).all()

    def delete(self):
        """Delete the diet suggestion from database."""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<DietSuggestion User={self.user_id} Summary='{self.summary}'>"
