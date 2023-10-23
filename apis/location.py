from fastapi import Depends
from dependencies.auth import get_current_user
import models.location
import models.user
from apis.base import QiQiBaseRouter
from apis.documentedresponse import JDR204, JDR400, create_documentation

class LocationApi(QiQiBaseRouter):
    """ Location API """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        @self.post('/traffic')
        async def get_traffic(area: models.location.Area, user: models.user.User = Depends(get_current_user)):
            if not await self.services.location.get_traffic(area):
                return JDR400.response()
            return JDR204.response()
        
        @self.post('/location', description='Upload user\'s current location', **create_documentation(JDR204, JDR400))
        async def upload_location(location: models.location.Location, user: models.user.User = Depends(get_current_user)):
            if not await self.services.location.upload_location(user.id, location):
                return JDR400.response()
            return JDR204.response()
        
        @self.get('/location/{user_id}')
        async def get_friend_location(user_id: int):
            return await self.location_service.get_friend_location_service(user_id)

        # @self.get('/bikes_around_me/{location}')
        # async def CreateRedZoneMap(my_lat: float, my_long: float):
        #     activeuser_location = await self.location_service.get_all_bikes()

        #     await self.location_service.find_redzone(activeuser_location, my_lat, my_long)

        #     return FileResponse('savedmaps/redzoneimage.png')


