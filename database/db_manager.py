import streamlit as st
from datetime import datetime
from typing import Dict, List
import hashlib
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from config import MONGODB_URI

class DatabaseManager:
    def __init__(self):
        """Initialize MongoDB connection."""
        self.client = MongoClient(MONGODB_URI)
        self.db: Database = self.client.get_database()
        self.users: Collection = self.db.users
        self.cheques: Collection = self.db.cheques
        
        # Create unique index on username
        self.users.create_index("username", unique=True)
        
    def clear_session_results(self):
        """Clear the current session results."""
        if 'current_results' in st.session_state:
            st.session_state.current_results = []
        
    def verify_user(self, username: str, password: str) -> bool:
        """Verify user credentials against MongoDB."""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = self.users.find_one({"username": username})
        if user and user["password"] == hashed_password:
            # Clear any existing results when user logs in
            self.clear_session_results()
            return True
        
        return False
    
    def create_user(self, username: str, password: str, email: str) -> bool:
        """Create a new user in the database."""
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user_data = {
                "username": username,
                "password": hashed_password,
                "email": email,
                "created_at": datetime.utcnow(),
                "last_login": datetime.utcnow()
            }
            self.users.insert_one(user_data)
            return True
        except DuplicateKeyError:
            return False
    
    def save_cheque_data(self, data: List[Dict], username: str) -> List[str]:
        """Save multiple cheque data entries to MongoDB."""
        for entry in data:
            entry['timestamp'] = datetime.utcnow()
            entry['user'] = username
        
        result = self.cheques.insert_many(data)
        return [str(id) for id in result.inserted_ids]
    
    def get_user_cheques(self, username: str) -> List[Dict]:
        """Retrieve cheque data for a specific user."""
        return list(self.cheques.find({"user": username}))
    
    def clear_user_data(self, username: str):
        """Clear all cheque data for a specific user."""
        self.cheques.delete_many({"user": username})
    
    def update_last_login(self, username: str):
        """Update user's last login timestamp."""
        self.users.update_one(
            {"username": username},
            {"$set": {"last_login": datetime.utcnow()}}
        )