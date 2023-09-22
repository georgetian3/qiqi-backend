""" QiQi API """

import fastapi
from starlette.responses import RedirectResponse

class Api(fastapi.FastAPI):
    """ QiQi API """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        @self.get('/')
        async def docs():
            return RedirectResponse('/docs')
        @self.get('/health')
        async def health():
            return 'ok'


        