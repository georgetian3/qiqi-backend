from sqlmodel import SQLModel, Field

UserID = int



class User(SQLModel, table=True):
    __tablename__ = 'user'
    id: UserID = Field(primary_key=True)
    username: str
    password_hash: str
    email: str