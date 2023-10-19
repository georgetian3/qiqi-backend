import fastapi
from starlette.responses import RedirectResponse

from services.services import QiQiServices

class QiQiBaseRouter(fastapi.APIRouter):
    def __init__(self, services: QiQiServices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.services = services

# class QiQiBaseApi(fastapi.FastAPI):
    
