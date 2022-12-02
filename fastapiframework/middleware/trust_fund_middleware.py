from fastapi import Request
from strivelogger import StriveLogger

from fastapiframework.api.request_context import set_trust_fund_id
from fastapiframework.api.responses import abort_bad_request


def check_trust_fund_id(request: Request) -> None:
    value = request.headers.get("X-Trust-Fund-Id", None)

    if value:
        try:
            trust_fund_id = int(value)
            set_trust_fund_id(request, trust_fund_id)
        except BaseException:
            StriveLogger.error("Header X-Trust-Fund-Id is invalid")
            abort_bad_request(request)
    else:
        abort_bad_request(request)
