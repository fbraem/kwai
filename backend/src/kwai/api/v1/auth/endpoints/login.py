from datetime import datetime

from fastapi import APIRouter, Depends, status, Response, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel

from kwai.core.db.database import get_database
from kwai.core.domain.value_objects import InvalidEmailException
from kwai.core.settings import get_settings
from kwai.modules.identity import (
    AuthenticateUser,
    AuthenticateUserCommand,
    AuthenticationException,
)
from kwai.modules.identity.tokens import (
    AccessTokenDbRepository,
    RefreshTokenDbRepository,
)
from kwai.modules.identity.users import UserAccountDbRepository


class JsonUserAttributes(BaseModel):
    name: str
    email: str


class JsonUserData(BaseModel):
    id: str
    type: str = "users"
    attributes: JsonUserAttributes


class JsonUserDocument(BaseModel):
    data: JsonUserData


class TokenSchema(BaseModel):
    """The schema for an access/refresh token."""

    access_token: str
    refresh_token: str
    expiration: str


router = APIRouter()


@router.post(
    "/login",
    response_model=TokenSchema,
    summary="Create access and refresh token for a user.",
)
async def login(
    settings=Depends(get_settings),
    db=Depends(get_database),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    command = AuthenticateUserCommand(
        username=form_data.username, password=form_data.password
    )

    try:
        refresh_token = AuthenticateUser(
            UserAccountDbRepository(db),
            AccessTokenDbRepository(db),
            RefreshTokenDbRepository(db),
        ).execute(command)
    except InvalidEmailException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email address"
        )
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    return {
        "access_token": jwt.encode(
            {
                "iat": refresh_token().access_token().traceable_time.created_at,
                "exp": refresh_token().access_token().expiration,
                "jti": str(refresh_token().access_token().identifier),
                "sub": str(refresh_token().access_token().user_account().user.uuid),
                "scope": [],
            },
            settings.jwt_secret,
            settings.jwt_algorithm,
        ),
        "refresh_token": jwt.encode(
            {
                "iat": refresh_token().traceable_time.created_at,
                "exp": refresh_token().expiration,
                "jti": str(refresh_token().identifier),
            },
            settings.jwt_refresh_secret,
            settings.jwt_algorithm,
        ),
        "expiration": refresh_token()
        .access_token()
        .expiration.isoformat(" ", "seconds"),
    }
