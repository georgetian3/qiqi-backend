import fastapi
from services.services import QiQiServices
from starlette.responses import RedirectResponse


class QiQiBaseApi(fastapi.FastAPI):
    def __init__(self, services: QiQiServices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.services = services

        @self.get('/')
        async def docs():
            return RedirectResponse('/docs')
