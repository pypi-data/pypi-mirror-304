import jwt
import datetime
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from textwrap import wrap

class AuthService:
    algorithm = "RS256"  # Algoritmo predeterminado

    @staticmethod
    def generate_token(payload: dict, private_key: str, expiration: int = 3600):
        """Genera un token JWT con una expiración determinada."""
        payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)
        return jwt.encode(payload, private_key, algorithm=AuthService.algorithm)

    @staticmethod
    def format_public_key(public_key_str: str) -> str:
        """Formatea una cadena de clave pública para asegurarse de que esté en formato PEM válido."""
        # Elimina espacios en blanco al inicio y al final
        public_key_str = public_key_str.strip()

        # Verifica si la clave ya contiene los encabezados y pies de formato PEM
        if not public_key_str.startswith("-----BEGIN PUBLIC KEY-----"):
            public_key_str = "-----BEGIN PUBLIC KEY-----\n" + public_key_str
        if not public_key_str.endswith("-----END PUBLIC KEY-----"):
            public_key_str += "\n-----END PUBLIC KEY-----"

        # Divide la clave en líneas de 64 caracteres para cumplir con el formato PEM
        lines = public_key_str.splitlines()
        key_body = ''.join(lines[1:-1])  # Junta el contenido sin los encabezados y pies
        key_body = "\n".join(wrap(key_body, 64))  # Formatea el cuerpo en líneas de 64 caracteres

        # Reconstruye la clave en formato PEM
        pem_formatted_key = f"{lines[0]}\n{key_body}\n{lines[-1]}"
        return pem_formatted_key

    @staticmethod
    def verify_token(token: str, public_key: str):
        """Verifica y decodifica un token JWT usando la clave pública."""
        try:
            pem_formatted_key = AuthService.format_public_key(public_key)
            return jwt.decode(token, pem_formatted_key, algorithms=[AuthService.algorithm])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def verify_authorization_header(authorization: str, public_key: str):
        """Verifica el encabezado de autorización."""
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
            token_data = AuthService.verify_token(token, public_key)
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