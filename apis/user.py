import fastapi

class UserApi(fastapi.FastAPI):
    """ User API """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        @self.get('/user')
        async def user():
            return 'user'
        
        @self.post('/user')
        async def user():
            return await self.user_service.create_user()