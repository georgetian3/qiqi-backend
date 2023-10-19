""" QiQi API """

from fastapi.responses import RedirectResponse
from apis.location import LocationApi
from apis.user import UserApi
from fastapi import FastAPI

class QiQiApi(FastAPI):
    """ QiQi API """
    VERSION = '/v1'
    def __init__(self, *args, **kwargs):
        super().__init__(title='QiQi API', *args, **kwargs)

        self.include_router(UserApi(*args, **kwargs), prefix=QiQiApi.VERSION)
        self.include_router(LocationApi(*args, **kwargs), prefix=QiQiApi.VERSION)

        @self.get('/')
        async def docs():
            return RedirectResponse('/docs')
        
