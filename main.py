from apis.api import QiQiApi

import models.database

import services.user
import services.location

from config import Config

import argparse

config = Config()
db = models.database.Database(config.DATABSE_URL)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()
    if args.reset:
        db.reset()
        exit()

user_service = services.user.UserService(db, config)
location_service = services.location.LocationService(db, config)
api = QiQiApi(user_service, location_service)