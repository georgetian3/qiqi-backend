from typing import NamedTuple

class QiQiConfig(NamedTuple):
    SECRET_KEY: str = '' # openssl rand -hex 32
    ALGORITHM: str = 'HS256'
    DATABSE_URL: str = 'sqlite+aiosqlite:///./qiqi.db'