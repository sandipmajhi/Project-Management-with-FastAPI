from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config.db import conn
from .auth_handler import decode_jwt
from fastapi.responses import JSONResponse


class JWTBearer(HTTPBearer):
    """
    Custom JWT Bearer authentication class.

    This class inherits from FastAPI's HTTPBearer and provides a custom implementation
    for verifying JWT tokens.

    Args:
        auto_error (bool, optional): Whether to automatically raise an error if the token is invalid. Defaults to True.

    Raises:
        HTTPException: If the token is invalid, expired, or missing.
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        Verify the JWT token in the request.

        Args:
            request (Request): The incoming request.

        Returns:
            str: The verified JWT token.

        Raises:
            HTTPException: If the token is invalid, expired, or missing.
        """
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        """
        Verify the JWT token.

        Args:
            jwtoken (str): The JWT token to verify.

        Returns:
            bool: True if the token is valid, False otherwise.

        Raises:
            HTTPException: If the token is invalid or expired.
        """
        isTokenValid: bool = False

        try:
            present_in_login_db = conn.local.tokens.find_one({"access_token":jwtoken})
            
            if present_in_login_db is None:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
                
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid