""" QiQi API """

from apis.user import UserApi
from apis.location import LocationApi


        
class QiQiApi(
    UserApi,
    LocationApi   
):
    """ QiQi API """
    def __init__(self, *args, **kwargs):
        super().__init__(
            title='QiQi API',
            *args, **kwargs
        )

        