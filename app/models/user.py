from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db

class User(db.Model):
    """User Model representing application users."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    # cascade="all, delete-orphan" ensures child records are deleted when user is deleted
    poop_logs = db.relationship('PoopLog', backref='user', lazy=True, cascade="all, delete-orphan")
    diet_suggestions = db.relationship('DietSuggestion', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies the hashed password against the provided password."""
        return check_password_hash(self.password_hash, password)

    # --- CRUD Static & Class Methods ---
    @classmethod
    def create(cls, username, password):
        """Create a new user and save to database."""
        user = cls(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_by_id(cls, user_id):
        """Retrieve a user by their ID."""
        return cls.query.get(user_id)

    @classmethod
    def get_by_username(cls, username):
        """Retrieve a user by their username."""
        return cls.query.filter_by(username=username).first()

    def update(self, username=None, password=None):
        """Update user fields."""
        if username:
            self.username = username
        if password:
            self.set_password(password)
        db.session.commit()
        return self

    def delete(self):
        """Delete the user from database."""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.username}>"
