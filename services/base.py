from config import QiQiConfig
from models.database import QiQiDatabase


class QiQiBaseService:
    def __init__(self, config: QiQiConfig, database: QiQiDatabase):
        self.config = config
        self.database = database