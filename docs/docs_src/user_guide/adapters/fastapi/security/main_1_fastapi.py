from typing import Annotated, Any, Optional, Union
from uuid import UUID
import uuid

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from fastagency.adapters.fastapi import FastAPIAdapter
from fastagency.runtimes.autogen import AutoGenWorkflows

from .workflows import simple_workflow

wf = AutoGenWorkflows()

wf.register(name="simple_learning", description="Student and teacher learning chat")(simple_workflow)

app = FastAPI(title="FastAPI with FastAgency")

################################################################################
#
# Taken from https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
#

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret", # pragma: allowlist secret
        "disabled": False,
        "user_id": uuid.uuid4(),
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2", # pragma: allowlist secret
        "disabled": True,
        "user_id": uuid.uuid4(),
    },
}

def fake_hash_password(password: str) -> str:
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    user_id: UUID


class UserInDB(User):
    hashed_password: str


def get_user(db: dict[str, Any], username: str) -> Optional[UserInDB]:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None


def fake_decode_token(token: str) -> Optional[UserInDB]:
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> Optional[User]:
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> Optional[User]:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict[str, str]:
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


#
# End of code from https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
#
################################################################################

def get_user_id(
    current_user: Annotated[User, Depends(get_current_user)],
) -> Optional[UUID]:
    return current_user.user_id

adapter = FastAPIAdapter(provider=wf, get_user_id=get_user_id)
app.include_router(adapter.router)

# this is optional, but we would like to see the list of available workflows
@app.get("/")
def read_root() -> dict[str, dict[str, str]]:
    return {"Workflows": {name: wf.get_description(name) for name in wf.names}}
