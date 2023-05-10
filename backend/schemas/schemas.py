from pydantic import BaseModel


# class UserBase(BaseModel):
#     id: int


class UserEd(BaseModel):
    name: str | None = None
    info: str | None = None
    age: int | None = None
    email: str | None = None


class UserIn(UserEd):
    friends: list[int] = []


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserDB:
    def __init__(self):
        self.users = dict()

    def add_user(self, user: UserIn, id: int):
        self.users[id] = user

    def get_user(self, id: int) -> UserIn:
        return self.users[id]

    def get_next_id(self) -> int:
        return len(self.users) + 1


users = UserDB()
