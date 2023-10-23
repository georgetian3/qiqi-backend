""" QiQi API """

import json
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from apis.auth import AuthApi
from apis.location import LocationApi
from apis.user import UserApi


class QiQiApi(FastAPI):
    """ QiQi API """
    def __init__(self, *args, **kwargs):
        super().__init__(title='QiQi API', *args, **kwargs)
        self.include_router(AuthApi(*args, **kwargs), tags=['auth'])
        self.include_router(UserApi(*args, **kwargs), tags=['user'])
        self.include_router(LocationApi(*args, **kwargs), tags=['location'])

        @self.get('/')
        async def docs():
            return RedirectResponse('/docs')
        
    def get_openapi(self):
        with open('openapi.json', 'w') as f:
            json.dump(self.openapi(), f, indent=2)
