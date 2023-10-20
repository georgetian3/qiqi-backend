from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException

from apis.base import QiQiBaseRouter
from apis.documentedresponse import JDR, create_documentation
from models.auth import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')

class AuthApi(QiQiBaseRouter):
    """ User API """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username/email or password',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        token_200 = JDR(status.HTTP_200_OK, 'OK', Token)
        token_401 = JDR(status.HTTP_401_UNAUTHORIZED, self.credentials_exception.detail)
        @self.post('/token', **create_documentation(token_200, token_401))
        async def token(form_data: OAuth2PasswordRequestForm = Depends()):
            user = await self.services.user.authenticate(username_or_email=form_data.username, password=form_data.password)
            if not user:
                raise self.credentials_exception
            return token_200.response(
                Token(
                    access_token=self.services.auth.create_access_token(user.id),
                    token_type='bearer'
                )
            )
