import fastapi
from starlette.responses import RedirectResponse
from config import QiQiConfig

from services.services import QiQiServices


class QiQiBaseRouter(fastapi.APIRouter):
    def __init__(self, config: QiQiConfig, services: QiQiServices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.services = services
        self.config = config

# class QiQiBaseApi(fastapi.FastAPI):
    
