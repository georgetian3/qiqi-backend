""" QiQi API """

from apis.user import UserApi
from apis.location import LocationApi

from starlette.responses import RedirectResponse

import services.user
        
class QiQiApi(UserApi, LocationApi):
    """ QiQi API """
    def __init__(self, 
        user_service: services.user.UserService,      
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.user_service = user_service

        @self.get('/')
        async def docs():
            return RedirectResponse('/docs')
        @self.get('/health')
        async def health():
            return 'ok'