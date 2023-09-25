""" QiQi API """

from apis.user import UserApi
from apis.location import LocationApi

from starlette.responses import RedirectResponse

        
class QiQiApi(UserApi, LocationApi):
    """ QiQi API """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        @self.get('/')
        async def docs():
            return RedirectResponse('/docs')
        @self.get('/health')
        async def health():
            return 'ok'