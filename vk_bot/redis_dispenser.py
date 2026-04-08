from vkbottle import BaseStateGroup
from vkbottle.dispatch import BuiltinStateDispenser
from vkbottle.dispatch.dispenser.base import StatePeer

from vk_bot.states import States
from storage.db import RedisDB


class RedisStateDispenser(BuiltinStateDispenser):
    def __init__(self, storage: RedisDB):
        super().__init__()

        self.storage = storage

    async def get(self, peer_id: int) -> StatePeer | None:
        result = await self.storage.get(peer_id)

        if result is None:
            return None

        state = result[0]
        payload = result[1]

        return StatePeer(
            peer_id=peer_id,
            state=States(state),
            payload=payload
        )

    async def set(self, peer_id: int, state: BaseStateGroup, **payload):
        await self.storage.set(peer_id, state.value, **payload)

    async def delete(self, peer_id: int):
        await self.storage.delete(peer_id)
