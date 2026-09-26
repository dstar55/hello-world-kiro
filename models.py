"""
Database models for user authentication and authorization.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    User model for storing user information and authentication data.
    
    Attributes:
        id: Primary key
        email: User's Gmail address (unique)
        name: User's full name from Google profile
        profile_picture: URL to user's Google profile picture
        role: User role (superadmin or user)
        status: Account status (pending, approved, rejected)
        created_at: Timestamp when user registered
        updated_at: Timestamp when user record was last updated
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(500), nullable=True)
    role = db.Column(db.String(50), nullable=False, default='user')  # 'superadmin' or 'user'
    status = db.Column(db.String(50), nullable=False, default='pending')  # 'pending', 'approved', 'rejected'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def is_superadmin(self):
        """Check if user is a superadmin."""
        return self.role == 'superadmin'
    
    def is_approved(self):
        """Check if user is approved."""
        return self.status == 'approved'
    
    def is_pending(self):
        """Check if user is pending approval."""
        return self.status == 'pending'
    
    def is_rejected(self):
        """Check if user is rejected."""
        return self.status == 'rejected'
    
    def can_access_private_pages(self):
        """Check if user can access private pages (approved or superadmin)."""
        return self.is_approved() or self.is_superadmin()
    
    def to_dict(self):
        """Convert user object to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'profile_picture': self.profile_picture,
            'role': self.role,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
