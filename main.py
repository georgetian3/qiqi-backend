import argparse

import dependencies.auth
import models.database
from apis.apis import QiQiApi
from config import QiQiConfig
from services.services import QiQiServices

config = QiQiConfig()
database = models.database.QiQiDatabase(config.DATABSE_URL)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()
    if args.reset:
        database.reset()
        exit()

services = QiQiServices(config=config, database=database)
dependencies.auth.auth_service = services.auth
api = QiQiApi(services=services)