from sqlmodel import SQLModel

UserID = int
class User(SQLModel, table=True):
    id: UserID
    username: str
    password_hash: str
    email: str