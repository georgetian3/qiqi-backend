from services.user import UserService
from services.location import LocationService
from config import QiQiConfig
from models.database import QiQiDatabase


class QiQiServices:
    """ QiQiServices """
    
    def __init__(self, config: QiQiConfig, database: QiQiDatabase):
        self.user = UserService(config, database)
        self.location = LocationService(config, database)