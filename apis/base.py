import fastapi
import services.user
import services.location

class QiQiBaseApi(fastapi.FastAPI):
    def __init__(self, 
        user_service: services.user.UserService,
        location_service: services.location.LocationService,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.user_service = user_service
        self.location_service = location_service