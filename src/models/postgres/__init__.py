from src.models.postgres.base import get_session, set_session, Base, get_async_session
from src.models.postgres.post import PostModel
from src.models.postgres.user import UserModel

set_session()
