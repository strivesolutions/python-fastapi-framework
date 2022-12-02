from typing import Optional

from fastapi import HTTPException, Request
from starlette import status
from strivelogger import StriveLogger

from fastapiframework.models.camel_case_model import CamelCaseModel


def _create_error_detail(message: str, path: str, error_code: int) -> dict:
    return {"error": {"message": message, "path": path, "code": error_code}}


def abort_bad_request(request: Request, exception: Optional[Exception] = None) -> None:
    StriveLogger.error(f"{request.url}: {exception or 'bad request'}")

    code = (
        getattr(exception, "code", status.HTTP_400_BAD_REQUEST)
        if exception
        else status.HTTP_400_BAD_REQUEST
    )

    detail = _create_error_detail(
        message="Bad Request", path=request.url.path, error_code=code
    )

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def abort_unauthorized(request: Request) -> None:
    detail = _create_error_detail(
        message="Unauthorized",
        path=request.url.path,
        error_code=status.HTTP_401_UNAUTHORIZED,
    )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


def abort_forbidden(request: Request) -> None:
    detail = _create_error_detail(
        message="Forbidden",
        path=request.url.path,
        error_code=status.HTTP_403_FORBIDDEN,
    )
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


def abort_internal_server_error(request: Request) -> None:
    detail = _create_error_detail(
        message="Internal Server Error",
        path=request.url.path,
        error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
    )


def abort_not_found(request: Request) -> None:
    detail = _create_error_detail(
        message="Not Found",
        path=request.url.path,
        error_code=status.HTTP_404_NOT_FOUND,
    )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def ok_response(data: CamelCaseModel) -> dict:
    return {"data": data}
