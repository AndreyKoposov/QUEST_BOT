from datetime import datetime


class User:
    __pk__ = 'peer_id'
    __colname__ = 'users'

    peer_id: int
    diamonds: int
    created_at: datetime

    def __init__(self, peer_id: int = -1, diamonds: int = 0):
        self.peer_id = peer_id
        self.diamonds = diamonds
        self.created_at = datetime.now()

class Game:
    __pk__ = 'peer_id'
    __colname__ = 'games'

    peer_id: int
    game: dict
    update_at: datetime

    def __init__(self, game: dict, peer_id: int = -1):
        self.peer_id = peer_id
        self.game = game
        self.update_at = datetime.now()
