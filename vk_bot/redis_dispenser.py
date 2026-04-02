import json
from vkbottle import BaseStateGroup
from vkbottle.dispatch import BuiltinStateDispenser
from vkbottle.dispatch.dispenser.base import StatePeer
from redis.asyncio import Redis

from vk_bot.states import States


class RedisStateDispenser(BuiltinStateDispenser):
    def __init__(self, redis_client: Redis):
        super().__init__()

        self.redis = redis_client

    async def get(self, peer_id: int) -> StatePeer | None:
        key = self._make_key(peer_id)
        data = await self.redis.get(key)

        if data is None:
            return None

        parsed = json.loads(data)
        state = parsed.get("state")
        payload = parsed.get("payload", {})

        return StatePeer(
            peer_id=peer_id,
            state=States(state),
            payload=payload
        )

    async def set(self, peer_id: int, state: BaseStateGroup, **payload):
        key = self._make_key(peer_id)
        data = json.dumps({
            "state": state.value,
            "payload": payload
        }, default=str)

        await self.redis.set(key, data)

    async def delete(self, peer_id: int):
        key = self._make_key(peer_id)
        await self.redis.delete(key)

    def _make_key(self, peer_id: int):
        return f'state<{peer_id}>'
