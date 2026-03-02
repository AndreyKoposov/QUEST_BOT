import sqlalchemy as db
from app.config import ENV


class Driver():
    def __init__(self) -> None:
        self.engine = db.create_engine(ENV.DATABASE_URL.encoded_string())
        self.connection = self.engine.connect()

        self.connection.close()
