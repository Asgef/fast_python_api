from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from fast_python_api.chemas.user_crud import UserPublic, UserCreate, UserUpdate, LoginUpdate, NameUpdate
from fast_python_api.models import User, Login, Name
from fast_python_api.database import async_session
from fast_python_api.auth.hashing import get_password_hash
from fast_python_api.core.user_db import email_exists, username_exists, get_user_by_id
import uuid
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(
        user_data: UserCreate,
        session: AsyncSession
) -> UserPublic:
    if await email_exists(user_data.email, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    if await username_exists(user_data.login.username, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    user_uuid = str(uuid.uuid4())

    user = User(
        id=user_uuid,
        **user_data.model_dump(exclude={"login", "name"}),

    )
    name = Name(
        user_id=user_uuid,
        **user_data.name.model_dump()
    )
    login = Login(
        uuid=user_uuid,
        username=user_data.login.username,
        password=get_password_hash(user_data.login.password)
    )

    session.add_all([
        user, login, name
    ])
    await session.commit()
    await session.refresh(user)
    return UserPublic(**user.to_dict())


async def update_user(
        user_id: uuid.UUID,
        update_data: UserUpdate,
        session: AsyncSession
) -> UserPublic:
    user = await get_user_by_id(user_id, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    for key, value in update_data.model_dump(exclude_unset=True).items():
        if key not in ["name", "login"]:
            setattr(user, key, value)

    if update_data.name:
        if not user.name:
            user.name = Name(user_id=user.id, **update_data.name.model_dump())
        else:
            for key, value in update_data.name.model_dump(
                    exclude_unset=True
            ).items():
                setattr(user.name, key, value)

    if update_data.login:
        if not user.login:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User has no login data"
            )

        if update_data.login.username:
            user.login.username = update_data.login.username

        if update_data.login.password:
            user.login.password = get_password_hash(update_data.login.password)

    await session.commit()
    result = await session.execute(
        select(User).options(joinedload(User.name),
                             joinedload(User.login)
                             ).where(User.id == str(user_id))
    )
    user = result.scalars().first()
    return UserPublic(**user.to_dict())
