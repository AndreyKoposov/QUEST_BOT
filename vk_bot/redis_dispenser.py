import json
from json import JSONDecodeError
from vkbottle import BaseStateGroup
from vkbottle.dispatch import BuiltinStateDispenser
from vkbottle.dispatch.dispenser.base import StatePeer
from redis.asyncio import Redis

from vk_bot.states import States


class RedisStateDispenser(BuiltinStateDispenser):
    def __init__(self, redis_client: Redis):
        super().__init__()

        self.ttl = 3600
        self.redis: Redis = redis_client

    def _make_key(self, peer_id: int):
        return f'//{peer_id}'

    async def get(self, peer_id: int) -> StatePeer | None:
        key = self._make_key(peer_id)
        data = await self.redis.get(key)

        if data is None:
            return None

        try:
            parsed = json.loads(data)
            state = parsed.get("state")
            payload = parsed.get("payload", {})

            if state is None:
                return None

            return StatePeer(
                peer_id=peer_id,
                state=States(state),
                payload=payload
            )
        except (JSONDecodeError, TypeError):
            return None

    async def set(self, peer_id: int, state: BaseStateGroup, **payload):
        if hasattr(state, "value"):
            state_value = state.value
        else:
            state_value = state

        key = self._make_key(peer_id)
        data = json.dumps({
            "state": state_value,
            "payload": payload
        }, default=str)

        await self.redis.setex(key, self.ttl, data)

    async def delete(self, peer_id: int):
        key = self._make_key(peer_id)
        await self.redis.delete(key)
