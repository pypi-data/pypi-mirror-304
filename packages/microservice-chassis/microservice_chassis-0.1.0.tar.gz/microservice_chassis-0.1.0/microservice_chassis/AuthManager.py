import jwt
import datetime
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

class AuthService:
    def __init__(self, private_key: str, public_key: str, algorithm="RS256"):
        self.private_key = private_key
        self.public_key = public_key
        self.algorithm = algorithm

    def generate_token(self, payload: dict, expiration: int = 3600):
        payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)
        return jwt.encode(payload, self.private_key, algorithm=self.algorithm)

    def verify_token(self, token: str):
        try:
            return jwt.decode(token, self.public_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def verify_authorization_header(self, authorization: str):

        if not authorization:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization header missing"}
            )

        token = authorization.split(" ")[1] if len(authorization.split(" ")) == 2 else None
        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid Authorization header format"}
            )

        try:
            token_data = self.verify_token(token)
            if not token_data:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid or expired token"}
                )
            return token_data
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
