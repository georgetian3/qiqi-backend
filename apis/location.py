import fastapi

        
class LocationApi(fastapi.FastAPI):
    """ Location API """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        @self.get('/location')
        async def location():
            return 'location'