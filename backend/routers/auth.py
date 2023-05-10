import os
from datetime import timedelta, datetime
from dotenv import load_dotenv
from fastapi.openapi.models import Response
from jose import JWTError, jwt
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import bcrypt
from starlette.responses import HTMLResponse, JSONResponse
from backend.schemas.schemas import users
from veiws.veiw import html1

load_dotenv()
SECRET = os.getenv('SECRET')
ALGORITHM = os.getenv('ALGORITHM')
if ALGORITHM is None:
    ALGORITHM = 'HS256'
if SECRET is None:
    SECRET = 'secret'
ACCESS_TOKEN_EXPIRE_MINUTES1 = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
if ACCESS_TOKEN_EXPIRE_MINUTES1:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES1)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter(
    prefix="/auth", tags=["auth"], responses={404: {"description": "Not found"}}
)


class PassDB:
    def __init__(self):
        self.passwords = dict()

    def add_password(self, id: int, password: str) -> str:
        if id in self.passwords:
            return "User already exist"
        salt = bcrypt.gensalt()
        if SECRET:
            password += SECRET
        self.passwords[id] = bcrypt.hashpw(password.encode(), salt)
        return "OK"

    def check(self, id: int, password: str) -> bool:
        if id not in self.passwords:
            return False
        if SECRET:
            password += SECRET
        if bcrypt.checkpw(password.encode(), self.passwords[id]):
            return True
        else:
            return False


passwords = PassDB()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        id: int = payload.get("id")
        if id is None:
            raise credentials_exception
        # token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # user = users.get_user(id)
    if id not in users.users:
        raise credentials_exception
    return id


@router.post("/token", response_model=Response)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    if (
        passwords.check(int(form_data.username), form_data.password)
        and int(form_data.username) in users.users
    ):
        # user = users.get_user(int(form_data.username))
        pass
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": int(form_data.username)}, expires_delta=access_token_expires
    )
    content = {"access_token": access_token, "token_type": "Bearer"}
    response = JSONResponse(content=content)
    token = 'Bearer ' + access_token
    response.set_cookie(key="Authenticate", value=token)
    return response


@router.get("/login")
async def get1():
    return HTMLResponse(html1)
