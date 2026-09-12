import jwt
from datetime import datetime, timedelta, timezone

def generate_jwt(id: int) -> str:
    payload = {
        "sub": str(id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    
    """ TODO: Will replace with env variable later """
    secret_key = "a-powerful-secret-key"
    
    return jwt.encode(payload, secret_key, algorithm="HS256")
