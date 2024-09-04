import time
from typing import Dict
from config.db import conn
import jwt
from decouple import config
import threading


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

ACCESS_TOKEN = ""
def token_response(token: dict):
    return {
        "access_token": token["access_token"],
        "refresh_token": token["refresh_token"]
    }

def sign_jwt(user_id: str) -> Dict[str, str]:
    global ACCESS_TOKEN
    payload = {
        "user_id": user_id,
        "expires": time.time() + 3000
    }
    access_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    refresh_token = jwt.encode({"user_id":user_id}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    ACCESS_TOKEN = access_token
    return token_response({"access_token":access_token, "refresh_token":refresh_token})

def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decoded_token["expires"] >= time.time():
            return decoded_token  
        else: 
            conn.local.tokens.delete_one({"access_token":token})
            return None
    except Exception as e:
        return {e}
    

def check_token_periodically():
    while True:
        time.sleep(10)

# Start the token checking loop in a separate thread
thread = threading.Thread(target=check_token_periodically, daemon=True)
thread.start()

