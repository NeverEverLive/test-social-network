from typing import List
import itertools as it

from sqlalchemy import select, update, delete
from pydantic import parse_obj_as
import bcrypt

from src.exceptions.user import UserNotExist
from src.models.postgres.user import UserModel
from src.models.postgres.base import get_session
from src.components.user.schemas import UserLogin, UserSchema
from src.components.user.schemas import UserResponse
from src.components.user.schemas import UsersResponse
from src.components.user.schemas import UserSecure
from src.components.auth.jwt_handler import encode_jwt_token


def signup_user(user: UserSchema) -> UserResponse:
    """Signup user.
    :type user: UserSchema
    :param user: User data
    :return: UserResponse with new user instance
    """
    user_query = UserModel().fill(**user.dict())
    
    with get_session() as session:
        session.add(user_query)
        session.commit()
    
    return UserResponse(
        user=user,
        message="User successfully signed up",
        success=True
        )


def get_users() -> UsersResponse:
    """Get users.
    :return: UsersResponse with all users
    """
    user_state = select(
        UserModel.id,
        UserModel.username,
    )

    with get_session() as session:
        print(list(it.chain(*session.execute(user_state).fetchall())))
        return UsersResponse(
            users=parse_obj_as(List[UserSecure], session.execute(user_state).fetchall()),
            message="Users collected successfully",
            success=True
        )


def get_user(id: str) -> UserResponse:
    """Get user.
    :type id: str
    :param id: User id
    :return: UserResponse with filtered user instance
    """
    user_state = select(
        UserModel.id,
        UserModel.username,
    ).where(
        UserModel.id == id
    )

    with get_session() as session:
        if user := session.execute(user_state).fetchone():
            return UserResponse(
                user=user,
                message="User successfully received",
                success=True
            )
        raise UserNotExist(
            status_code=404,
            message="This user doesn't exist"
        )


def update_user(user: UserSchema) -> UserResponse:
    """Update user.
    :type user: UserSchema
    :param user: Updated user data
    :return: UserResponse with updated user instance
    """
    user_state = update(
        UserModel
    ).where(
        UserModel.id == user.id
    ).values(
        **user.dict()
    )

    with get_session() as session:
        session.execute(user_state)
        session.commit()

    return UserResponse(
        user=user,
        message="User successfully updated",
        success=True
    )


def delete_user(id: str) -> UserResponse:
    """Delete user.
    :type id: str
    :param id: User id
    :return: UserResponse with message about operation
    """
    user_state = delete(
        UserModel
    ).where(
        UserModel.id == id
    )

    with get_session() as session:
        session.execute(user_state)
        session.commit()

    return UserResponse(
        message="User successfully deleted",
        success=True
    )


def login_user(user: UserLogin) -> UserResponse:
    """Login user.
    :type user: UserLogin
    :param id: User logging data
    :return: UserResponse with loggined user instance
    """
    user_state = select(
        UserModel
    ).where(
        UserModel.username == user.username
    )

    with get_session() as session:
        try: 
            user_state = session.execute(user_state).fetchone()[0]
        except TypeError:
            raise ValueError("This user doesn't exist")

    print(user_state)

    if not bcrypt.checkpw(user.hash_password, user_state.hash_password):
        raise ValueError('Invalid password')

    token = encode_jwt_token(user_state.id)

    return UserResponse(
        user=UserSecure.from_orm(user_state),
        message="You're successfully logined",
        success=True
    ), token
