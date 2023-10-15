""" QiQi API """

from apis.location import LocationApi
from apis.user import UserApi


class QiQiApi(
    UserApi,
    LocationApi,
):
    """ QiQi API """
    def __init__(self, *args, **kwargs):
        super().__init__(
            title='QiQi API',
            *args, **kwargs
        )

        