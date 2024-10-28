# Register routes

The register router will generate a `/register` route to allow a user to create a new account.

Check the [routes usage](../../usage/routes.md) to learn how to use them.

## Setup

```py
import uuid

from fastapi import FastAPI
from fastapi_users_with_username import FastAPIUsers

from .db import User
from .schemas import UserCreate, UserRead

fastapi_users_with_username = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()
app.include_router(
    fastapi_users_with_username.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
```
