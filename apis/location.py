import fastapi

from fastapi.responses import FileResponse
        
class LocationApi(fastapi.FastAPI):
    """ Location API """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        @self.get('/location')
        async def location():
            return 'location'
        
        @self.post('/update_location/{user_id_and_location}')
        async def update_location(id: int, lat: float, long: float):
            return await self.location_service.update_location_service(id, lat, long)

            # return("location updated to lat = {}, long = {}".format(lat, long))
        
        @self.get('/get_friend_location/{user_id}')
        async def get_friend_location(id: int):
            return await self.location_service.get_friend_location_service

        @self.get('/bikes_around_me/{location}')
        async def CreateRedZoneMap(my_lat: float, my_long: float):
            activeuser_location = await self.location_service.get_all_bikes()

            await self.location_service.find_redzone(activeuser_location, my_lat, my_long)

            return FileResponse('savedmaps/redzoneimage.png')


