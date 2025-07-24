from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError, BaseModel
from starlette.requests import Request

from src.common.core.config import settings

# reusable_oauth2 = OAuth2PasswordBearer(
#     tokenUrl=f"{settings.API_V1_STR}/login/access-token"
# )

class CurrentUser(BaseModel):
    """用户信息"""
    user_id: str
    # exp: int  # token 到期时间

class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        # return HTTPAuthorizationCredentials(scheme="bearer", credentials="3df33120efc146119b861331ac658a48")
        authorization: str = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


security = CustomHTTPBearer()
TOKEN_CACHE_KEY_PREFIX = "oauth2_access_token:"
# SessionDep = Annotated[Session, Depends(get_db)]
# TokenDep = Annotated[str, Depends(reusable_oauth2)]


# def get_current_user(session: SessionDep, token: TokenDep) -> User:
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
#         )
#         token_data = TokenPayload(**payload)
#     except (InvalidTokenError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#         )
#     user = session.get(User, token_data.sub)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     if not user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return user

async def get_current_user(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> CurrentUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    if not credentials.credentials:
        raise credentials_exception
    return CurrentUser(user_id=str(1))
    # key = TOKEN_CACHE_KEY_PREFIX + credentials.credentials
    # user_data = redis_client.get(key)
    # if user_data is None:
    #     raise credentials_exception
    # try:
    #     user_dict = json.loads(user_data)
    #     user_id = user_dict.get("userId", 0)
    #     return CurrentUser(user_id=str(user_id))
    # except json.JSONDecodeError:
    #     raise credentials_exception

# CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> CurrentUser:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user