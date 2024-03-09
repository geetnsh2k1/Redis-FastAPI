class RedisServiceBaseMeta(type):
    def __new__(cls, name, bases, attrs):
        if name != 'RedisServiceBase':
            if 'SCHEMA' not in attrs or not isinstance(attrs['SCHEMA'], type):
                raise AttributeError(f"{name} class must define a 'schema' attribute.")
        return super().__new__(cls, name, bases, attrs)


class RedisServiceBase(metaclass=RedisServiceBaseMeta):
    async def add(self, *args, **kwargs) -> str:
        raise NotImplementedError()

    async def get(self, *args, **kwargs) -> str:
        raise NotImplementedError()
