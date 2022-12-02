from typing import List, Optional

from fastapi import Depends, FastAPI

from .config import get_subscriptions
from .subscription import Subscription


def add_dapr_subscribe_handler(app: FastAPI, pubsub_name: Optional[str]) -> None:
    if not pubsub_name:
        return

    app.add_api_route("/dapr/subscribe", subscribe_handler)  # type: ignore


async def subscribe_handler(
    subscriptions: List[Subscription] = Depends(get_subscriptions),
) -> List[Subscription]:
    return subscriptions
