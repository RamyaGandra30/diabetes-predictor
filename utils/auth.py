from pymongo import MongoClient
import os
import streamlit as st
import bcrypt

# ----------------------------
# Get Mongo URI
# ----------------------------
try:
    MONGO_URI = st.secrets["MONGO_URI"]
except:
    from dotenv import load_dotenv
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set")

# ----------------------------
# MongoDB Connection
# ----------------------------
client = MongoClient(MONGO_URI)
db = client["diabetes_app"]
users_collection = db["users"]

# ----------------------------
# Register User
# ----------------------------
def register_user(username, email, password):
    if users_collection.find_one({"username": username}):
        return False

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password  # stored as bytes
    })
    return True

# ----------------------------
# Login User
# ----------------------------
def login_user(username, password):
    user = users_collection.find_one({"username": username})
    print(user)

    if user:
        stored_password = user["password"]

        # Convert BSON Binary to bytes
        stored_password = bytes(stored_password)

        if bcrypt.checkpw(password.encode(), stored_password):
            return user

    return None