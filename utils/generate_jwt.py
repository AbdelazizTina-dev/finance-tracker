import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv("JWT_SECRET")

def generate_jwt(id: int) -> str:
    payload = {
        "sub": str(id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    
    return jwt.encode(payload, secret_key, algorithm="HS256")
