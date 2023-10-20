import argparse
import asyncio

import dependencies.auth
import models.database
from apis.apis import QiQiApi
from config import QiQiConfig
from models.user import CreateUserRequest
from services.services import QiQiServices

config = QiQiConfig()
database = models.database.QiQiDatabase(config.DATABSE_URL)
services = QiQiServices(config=config, database=database)
dependencies.auth.services = services
api = QiQiApi(services=services)


def create_test_data():
    async def _create_test_data():
        await services.user.create_user(
            CreateUserRequest(
                username='testUser',
                password='testPassword',
            )
        )
    asyncio.run(_create_test_data())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', action='store_true')
    parser.add_argument('--create-test-data', action='store_true')
    args = parser.parse_args()
    if args.reset:
        database.reset()
    if args.create_test_data:
        create_test_data()