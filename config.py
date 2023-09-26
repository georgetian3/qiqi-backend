from typing import NamedTuple

# class DatabaseConfig(NamedTuple):
#     drivername: str = 'sqlite'
#     username: str = None
#     password: str = None
#     host: str = '/./qiqi.db'
#     port: int = None
#     database: str = None

class Config(NamedTuple):
    SECRET_KEY: str = '' # openssl rand -hex 32
    ALGORITHM: str = 'HS256'
    DATABSE_URL: str = 'sqlite+aiosqlite:///./qiqi.db'