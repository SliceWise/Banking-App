"""
Authentication module for the Banking Application
Handles user login, registration, and authentication
"""
import json
import os
import hashlib
import uuid
import datetime
import storage

def hash_password(password):
    """Create a secure hash of the password"""
    salt = uuid.uuid4().hex
    hashed = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    return f"{salt}:{hashed}"

def verify_password(stored_password, provided_password):
    """Verify the provided password against the stored hash"""
    salt, hashed = stored_password.split(':')
    calculated_hash = hashlib.sha256(salt.encode() + provided_password.encode()).hexdigest()
    return calculated_hash == hashed

def user_exists(username):
    """Check if a user already exists"""
    users = storage.load_users()
    return any(user['username'] == username for user in users)

def get_user(username):
    """Get user details by username"""
    users = storage.load_users()
    for user in users:
        if user['username'] == username:
            return user
    return None

def login(username, password):
    """Authenticate a user and return user details if successful"""
    user = get_user(username)
    if user and verify_password(user['password'], password):
        # Update last login timestamp
        user['last_login'] = datetime.datetime.now().isoformat()
        storage.save_users(storage.load_users())  # Save the updated users
        return user
    return None

def register(username, password, name, email):
    """Register a new user"""
    if user_exists(username):
        return None
    
    # Create new user
    new_user = {
        'username': username,
        'password': hash_password(password),
        'name': name,
        'email': email,
        'created_at': datetime.datetime.now().isoformat(),
        'last_login': datetime.datetime.now().isoformat()
    }
    
    users = storage.load_users()
    users.append(new_user)
    
    if storage.save_users(users):
        return new_user
    return None
