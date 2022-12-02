from typing import Any, Dict

from fastapi import Request


def set_claims(request: Request, claims: Dict[str, Any]) -> None:
    request.state.claims = claims


def get_claims(request: Request) -> Dict[str, Any]:
    claims = getattr(request.state, "claims", {})
    return claims


def set_trust_fund_id(request: Request, trust_fund_id: int) -> None:
    request.state.trust_fund_id = trust_fund_id


def get_trust_fund_id(request: Request) -> int:
    return getattr(request.state, "trust_fund_id", 0)
