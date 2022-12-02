from typing import Any, Dict, Optional

import jwt
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from strivelogger import StriveLogger

from fastapiframework.api.request_context import set_claims
from fastapiframework.api.responses import abort_unauthorized

# class AuthMiddleware(BaseHTTPMiddleware):
#     async def dispatch(
#         self, request: Request, call_next: RequestResponseEndpoint
#     ) -> Response:
#         check_token(request)
#         return await call_next(request)


def check_token(request: Request) -> None:
    token = __get_token(request)

    if not token:
        abort_unauthorized(request)

    set_claims(request, token)


def __get_token(request: Request) -> Optional[Dict[str, Any]]:
    if "Authorization" not in request.headers:
        return None

    header = request.headers["Authorization"]

    try:
        parts = header.split(" ")
        if len(parts) < 2:
            StriveLogger.warn("Invalid bearer token (less than 2 parts)")
            return None

        encoded = parts[1]
        token = jwt.decode(encoded, options={"verify_signature": False})
        return token

    except BaseException as ex:
        StriveLogger.error("Exception occurred while decoding token", exc_info=ex)
        return None
