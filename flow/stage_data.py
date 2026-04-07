from dataclasses import dataclass, field

from entities.party import Party
from entities.person import Person


@dataclass
class StageData:
    """
    Минимальный контекст, который получают Stage и logic-объекты.

    Stage не знает ни про UserSession, ни про FlowManager, ни про Menu.
    Вместо этого она получает только данные, которые реально нужны.

    messages:
        временный список служебных сообщений пользователю
        (например, ошибки валидации или подтверждения),
        который заполняется в process(), а отправляется уже FlowManager-ом.
    """
    chat_id: int
    people: list[Person] = None
    party: Party | None = None
    payload: dict[str, str] = field(default_factory=dict)
