from jose import jwt
from datetime import datetime, timedelta, timezone

def crear_token_conf(username:str = None, email: str = None):

    exp = datetime.now(timezone.utc) + timedelta(minutes=10)
    
    if not username is None or not email is None:

        payload = {
            "sub": email or username,
            "exp": int(exp.timestamp()),
            "iat": int(datetime.now(timezone.utc).timestamp()),
        }
        
        return jwt.encode(payload, 'secret', algorithm='HS256')
    
    return {"message": "Data invalid"}


def decode_token(token:str):
    payload  = jwt.decode(token, 'secret', algorithms=['HS256'])       
    
    data = payload.get("sub")

    if not data:
        return "Token inválido"

    return data