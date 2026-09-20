from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import FastAPI, HTTPException, Depends
from dotenv import load_dotenv
import os
import jwt

load_dotenv()
secret_key = os.getenv("JWT_SECRET")

security = HTTPBearer()
 
def get_current_user_id(auth: HTTPAuthorizationCredentials = Depends(security)) -> int:
    token = auth.credentials

    try:
        payload = jwt.decode(token, key=secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return int(payload["sub"])
