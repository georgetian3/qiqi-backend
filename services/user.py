from config import Config
import models.user
import models.database
import models.location
class UserService:

    def __init__(self, database: models.database.Database, config: Config):
        self.config = config
        self.database = database

    async def create_user(self) -> models.user.User:
        new_user = models.user.User(
            username='user15',
            password_hash='testpwhash',
            email='oo@mail.com',
            share_location=False
        )
        user_location_field = models.location.Location(
            location_lat=0,
            location_long=0
        )
        # TypeError: 'Session' object does not support the asynchronous context manager protocol
        async with self.database.async_session() as session:
            session.add(new_user)
            session.add(user_location_field)
            await session.commit()
        return new_user

    async def get_user(self, id_or_username: models.user.UserID | str) -> models.user.User:
        if isinstance(id_or_username, models.user.UserID):
            ...
        return models.user.User(
                id=0,
                usernaname='test',
                password_hash=None,
                email='test@georgetian.com'
        )
    