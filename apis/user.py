import fastapi

class UserApi(fastapi.FastAPI):
    """ User API """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        @self.get('/user')
        async def user():
            return 'user'