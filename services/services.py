from config import QiQiConfig
from models.database import QiQiDatabase
from services.auth import AuthService
from services.location import LocationService
from services.user import UserService


class QiQiServices:
    """ QiQiServices """
    
    def __init__(self, config: QiQiConfig, database: QiQiDatabase):
        self.auth = AuthService(config, database)
        self.user = UserService(config, database)
        self.location = LocationService(config, database)