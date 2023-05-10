from fastapi import (
    Form,
    HTTPException,
    Depends,
    APIRouter,
)
from backend.routers.auth import get_current_user, passwords
from backend.schemas.schemas import UserIn, UserEd
from backend.schemas.schemas import users

router = APIRouter(
    prefix="/user",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/users", tags=["users"])
async def users_list():
    if len(users.users) != 0:
        return users.users
    else:
        raise HTTPException(status_code=404, detail="Users not found")


@router.get("/{user_id}", response_model=UserIn, tags=["users"])
async def get_user(
    user_id: int, current_user_id: int = Depends(get_current_user)
):
    if user_id in users.users:
        if current_user_id != user_id:
            raise HTTPException(status_code=404, detail="No Access")
        return users.get_user(user_id)
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@router.post("/create", tags=["users"])
async def create_user(
    username: str = Form(),
    info: str = Form(),
    age: int = Form(),
    email: str = Form(),
    password: str = Form(),
):
    user = UserIn(name=username, info=info, age=age, email=email)
    user_id = users.get_next_id()
    users.add_user(user, user_id)
    passwords.add_password(user_id, password)
    return user_id


@router.post("/friend")
async def friend(
    id1: int = Form(),
    id2: int = Form(),
    current_user_id: int = Depends(get_current_user),
):
    if id1 != current_user_id and id2 != current_user_id:
        raise HTTPException(status_code=404, detail="No access")
    if id1 not in users.users or id2 not in users.users:
        raise HTTPException(status_code=404, detail="Users not found")
    if id1 in users.get_user(id2).friends:
        raise HTTPException(status_code=404, detail="Already friends")
    if id1 == id2:
        raise HTTPException(status_code=404, detail="Same user")

    users.get_user(id1).friends.append(id2)
    users.get_user(id2).friends.append(id1)
    return {"Status": "OK"}


@router.put("/edit/{user_id}")
async def edit(
    user_id: int, user: UserEd, current_user_id: int = Depends(get_current_user)
):
    if user_id in users.users:
        if current_user_id != user_id:
            raise HTTPException(status_code=404, detail="No Access")
        stored_user = users.get_user(user_id)
        update_data = user.dict(exclude_unset=True)
        updated_user = stored_user.copy(update=update_data)
        users.users[user_id] = updated_user
        return {"Status": "OK"}
    else:
        raise HTTPException(status_code=404, detail="Users not found")
