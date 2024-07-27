from fastapi import Header, HTTPException

STATIC_TOKEN = "xyz"

def authenticate(token: str = Header(...)):
    if token != STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token
