from fastapi import Response


def retriable_event_error(response: Response) -> dict:
    response.status_code = 500
    return {"status": "RETRY"}


def fatal_event_error(response: Response) -> dict:
    response.status_code = 404
    return {"status": "DROP"}
