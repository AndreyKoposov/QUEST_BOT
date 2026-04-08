from datetime import datetime


class User:
    __pk__ = 'peer_id'
    __colname__ = 'users'

    peer_id: int = -1
    diamonds: int = 0
    created_at: datetime = datetime.now()

    def __init__(self, peer_id: int = -1):
        self.peer_id = peer_id

class Game:
    __pk__ = 'peer_id'
    __colname__ = 'games'

    peer_id: int = -1
    game: dict = {}
    update_at: datetime = datetime.now()
