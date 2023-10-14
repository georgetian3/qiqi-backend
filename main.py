from apis.apis import QiQiApi
import models.database
from services.services import QiQiServices
from config import QiQiConfig
import argparse

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
api = QiQiApi(services)