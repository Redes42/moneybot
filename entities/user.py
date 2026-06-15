from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    chat_id: int = 0
    is_admin: bool = False
