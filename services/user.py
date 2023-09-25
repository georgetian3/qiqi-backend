from config import Config
import models.user
import models.database
class UserService:

    def __init__(self, database: models.database.Database, config: Config):
        self.config = config
        self.database = database

    async def create_user(self) -> models.user.User:
        new_user = models.user.User(
            username='test',
            password_hash='testpwhash',
            email='test@georgetian.com',
        )
        async with self.database.async_session() as session:
            session.add(new_user)
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
    