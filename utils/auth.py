from pymongo import MongoClient
import hashlib

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["diabetes_app"]
users_collection = db["users"]

# ----------------------------
# Password Hashing
# ----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ----------------------------
# Register User
# ----------------------------
def register_user(username, email, password):
    if users_collection.find_one({"username": username}):
        return False
    
    users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hash_password(password)
    })
    return True

# ----------------------------
# Login User
# ----------------------------
def login_user(username, password):
    user = users_collection.find_one({
        "username": username,
        "password": hash_password(password)
    })
    return user
