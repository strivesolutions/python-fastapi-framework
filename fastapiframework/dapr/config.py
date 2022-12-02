from typing import List

from .subscription import Subscription

subscriptions: List[Subscription] = []


def add_subscriptions(sub: Subscription) -> None:
    subscriptions.append(sub)


def get_subscriptions() -> List[Subscription]:
    return subscriptions
