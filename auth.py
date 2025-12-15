from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import re

# Mock user database
users = {
    "admin": {
        "username": "admin",
        "password": generate_password_hash("admin123"),
        "role": "admin"
    },
    "user": {
        "username": "user",
        "password": generate_password_hash("user123"),
        "role": "user"
    }
}

class AuthManager:
    """Authentication manager"""
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate user"""
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            return user
        return None
    
    @staticmethod
    def register_user(username, password, role='user'):
        """Register new user"""
        if username in users:
            return False, "Username already exists"
        
        if not re.match("^[a-zA-Z0-9_]{3,20}$", username):
            return False, "Invalid username format"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        users[username] = {
            "username": username,
            "password": generate_password_hash(password),
            "role": role
        }
        return True, "User registered successfully"

# Create a function to export create_access_token
def get_create_access_token():
    """Return the create_access_token function"""
    return create_access_token