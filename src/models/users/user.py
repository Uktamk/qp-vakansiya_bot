import msgspec
from datetime import datetime
from typing import Optional
from .user_session import UserQuestionnaireSession


class User(msgspec.Struct, kw_only=True):
    telegram_id: Optional[str]
    telegram_username: Optional[str]
    first_name: str
    phone_number: Optional[str]
    is_interviewed: bool
    is_blocked: bool
    created_at: datetime
    updated_at: datetime
    session: Optional[UserQuestionnaireSession]