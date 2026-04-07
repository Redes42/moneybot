from dataclasses import dataclass, field

from entities.party import Party
from entities.person import Person
from flow.stages import Stage


@dataclass
class UserSession:
    """
    Полное runtime-состояние пользователя.

    current_stage хранится как объект Stage. Это делает flow объектным
    внутри приложения.

    pending_payload нужен для тех случаев, когда перед InputStage требуется
    запомнить контекст ввода. Например:
    - для какого participant вводят coeff/payment
    - для какого person редактируют имя/coeff
    """
    chat_id: int
    current_stage: Stage
    people: list[Person] = field(default_factory=list)
    party: Party | None = None
    payload: dict[str, str] = field(default_factory=dict)
