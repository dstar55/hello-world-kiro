#!/usr/bin/env python3
"""
Superadmin Setup Script

This script allows you to create or update a superadmin user.
Run this script before starting the application for the first time.

Usage:
    python setup_superadmin.py
"""

import sys
import os
from getpass import getpass

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User


def validate_email(email):
    """Validate that email is a Gmail address."""
    if not email:
        return False, "Email cannot be empty"
    
    email = email.strip().lower()
    
    if '@' not in email:
        return False, "Invalid email format"
    
    if not email.endswith('@gmail.com'):
        return False, "Only Gmail addresses are allowed (must end with @gmail.com)"
    
    # Basic email validation
    local, domain = email.rsplit('@', 1)
    if not local or not domain:
        return False, "Invalid email format"
    
    return True, email


def setup_superadmin():
    """Interactive setup for superadmin account."""
    print("=" * 60)
    print("  🔐 SUPERADMIN SETUP")
    print("=" * 60)
    print()
    print("This script will set up a superadmin account for the application.")
    print("The superadmin can approve/reject user registrations.")
    print()
    
    # Get email address
    while True:
        email = input("Enter superadmin Gmail address: ").strip()
        
        valid, result = validate_email(email)
        if valid:
            email = result  # Use normalized email
            break
        else:
            print(f"❌ Error: {result}")
            print()
    
    print()
    print(f"📧 Email: {email}")
    
    # Confirm
    print()
    confirm = input("Create/update this user as superadmin? (yes/no): ").strip().lower()
    
    if confirm not in ['yes', 'y']:
        print()
        print("❌ Setup cancelled.")
        return
    
    print()
    print("⏳ Setting up database...")
    
    # Create app context and initialize database
    with app.app_context():
        # Create data directory if it doesn't exist
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f"✓ Created directory: {db_dir}")
        
        # Create tables
        db.create_all()
        print("✓ Database tables created")
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Update existing user
            old_role = user.role
            old_status = user.status
            
            user.role = 'superadmin'
            user.status = 'approved'
            db.session.commit()
            
            print()
            print("✓ User updated successfully!")
            print()
            print(f"  Email:  {user.email}")
            print(f"  Role:   {old_role} → superadmin")
            print(f"  Status: {old_status} → approved")
            
            if user.name:
                print(f"  Name:   {user.name}")
        else:
            # Create new user
            user = User(
                email=email,
                name='Superadmin',  # Will be updated on first login
                role='superadmin',
                status='approved'
            )
            db.session.add(user)
            db.session.commit()
            
            print()
            print("✓ Superadmin created successfully!")
            print()
            print(f"  Email:  {user.email}")
            print(f"  Role:   superadmin")
            print(f"  Status: approved")
            print()
            print("ℹ️  The user's name and profile picture will be updated")
            print("   when they first log in with Google.")
    
    print()
    print("=" * 60)
    print("  ✅ SETUP COMPLETE")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Make sure you have Google OAuth credentials configured")
    print("2. Start the application: python app.py")
    print("3. Log in with the superadmin Gmail account")
    print("4. Access the admin dashboard at /admin/dashboard")
    print()


def list_users():
    """List all users in the database."""
    print()
    print("=" * 60)
    print("  👥 CURRENT USERS")
    print("=" * 60)
    print()
    
    with app.app_context():
        users = User.query.order_by(User.created_at.desc()).all()
        
        if not users:
            print("No users found in the database.")
            print()
            return
        
        for user in users:
            print(f"📧 {user.email}")
            print(f"   Name:       {user.name or 'Not set'}")
            print(f"   Role:       {user.role}")
            print(f"   Status:     {user.status}")
            print(f"   Created:    {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            if user.updated_at:
                print(f"   Updated:    {user.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print()


def main():
    """Main entry point."""
    print()
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--list', '-l', 'list']:
            list_users()
            return
        elif sys.argv[1] in ['--help', '-h', 'help']:
            print("Usage:")
            print("  python setup_superadmin.py          # Interactive setup")
            print("  python setup_superadmin.py --list   # List all users")
            print("  python setup_superadmin.py --help   # Show this help")
            print()
            return
    
    try:
        setup_superadmin()
    except KeyboardInterrupt:
        print()
        print()
        print("❌ Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
