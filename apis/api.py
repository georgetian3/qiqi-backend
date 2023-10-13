""" QiQi API """

from apis.user import UserApi
from apis.location import LocationApi

from starlette.responses import RedirectResponse

import services.user
import services.location

        
class QiQiApi(UserApi, LocationApi):
    """ QiQi API """
    

        @self.get('/')
        async def docs():
            return RedirectResponse('/docs')
        @self.get('/health')
        async def health():
            return 'ok'