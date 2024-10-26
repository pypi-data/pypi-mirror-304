import random
from dataclasses import dataclass

from lanoel.utils import (
    has_duplicate_names,
    inner_category,
    max_count,
    outter_category,
)


@dataclass
class Participant:
    name: str
    category: str


@dataclass
class Pair:
    giver: str
    receiver: str


def secret_santa(participants: list[Participant]):

    if has_duplicate_names(participants):
        raise Exception(
            "Their are a duplicate name in the participants list.",
        )

    givers = participants.copy()
    receivers = participants.copy()

    pair = []
    while True:
        category = max_count(givers)

        inner = inner_category(givers, category)
        outter = outter_category(receivers, category)

        giver = random.choice(inner)
        receiver = random.choice(outter if len(outter) > 0 else participants)

        givers.remove(giver)
        receivers.remove(receiver)

        pair.append(Pair(giver.name, receiver.name))

        if len(givers) == 0:
            break

    return pair


if __name__ == "__main__":
    participants = [Participant("Oliver", "Tuner")]
    res = secret_santa(participants)
    print(res)
