from typing import NamedTuple


class QiQiConfig(NamedTuple):
    SECRET_KEY: str = '93b7ee730ce8290e1136bb74624fb7f0ba660b669e40df6b5637324c8ed443eb' # openssl rand -hex 32
    ALGORITHM: str = 'HS256'
    DATABSE_URL: str = 'sqlite+aiosqlite:///./qiqi.db'