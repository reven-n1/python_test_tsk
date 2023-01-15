from functools import wraps

from ..database import Database
from .exceptions import ValidationError


async def check_field_for_existence(order_by: str | None = None) -> str | None:
    """  checks if the specified field exists  """
    from .db_models import Statistic
    if order_by and order_by not in Statistic.get_model_columns(add_addition=True):
        raise ValidationError(typ=f'param - order_by', arg=f"value - {order_by}", msg='non allowed filter field', e_typ='value_error')
    return order_by


class SaveMixin:
    """ simplifies model saving (model.save())  """
    async def save(self):
        if self.id == None:
            async with await Database.get_class_session() as session:
                session.add(self)
                await session.commit()
                await session.refresh(self)


# in more complex projects, the choice will certainly be for the Redis
class Cache(object):
    _instance: 'Cache' = None
    __data = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Cache, cls).__new__(cls)
        return cls._instance

    def set_item(self, key, value):
        self.__data[key] = value

    def get_item(self, key):
        return self.__data.get(key, None)

    def reset_cache(self):
        self.__data = {}


def cache(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = Cache().get_item(tuple(kwargs.values()))
        if not result:
            result = await func(*args, **kwargs)
            Cache().set_item(tuple(kwargs.values()), result)
        return result
    return wrapper
