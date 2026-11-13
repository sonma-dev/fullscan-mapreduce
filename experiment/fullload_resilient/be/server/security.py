import os
import secrets
from typing import Optional

from fastapi import HTTPException
from starlette import status
from starlette.requests import HTTPConnection


API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("You haven't defined API_KEY.")
if len(API_KEY) < 32:
    raise RuntimeError("You must set API_KEY as a string with more than 32 characters.")


def extract_token(headers, query_params) -> Optional[str]:
    auth = headers.get("Authorization")
    if auth:
        parts = auth.split(" ", 1)
        if len(parts) == 2 and parts[0].lower() == "bearer":
            return parts[1].strip()

    x_api_key = headers.get("X-API-Key")
    if x_api_key:
        return x_api_key.strip()

    query_token = query_params.get("api_key")
    return query_token.strip() if query_token else None


async def verify_api_key(conn: HTTPConnection) -> str:
    token = extract_token(conn.headers, conn.query_params)
    if not token or not secrets.compare_digest(token, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return token

