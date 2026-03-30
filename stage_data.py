from dataclasses import dataclass, field

from domain.party import Party
from domain.person import Person


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
    people: list[Person]
    party: Party | None
    pending_payload: dict[str, str] = field(default_factory=dict)
    messages: list[str] = field(default_factory=list)
