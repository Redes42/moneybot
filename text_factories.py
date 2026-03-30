from bot.safe_sender import escape_html
from stage_data import StageData


def new_party_text_factory(data: StageData) -> str:
    if not data.party or not data.party.participants:
        return "Вечеринка создана.<br><br>Участники пока не добавлены."

    lines = ["<b>Участники:</b>"]
    for participant in data.party.participants:
        lines.append(
            f"• {escape_html(participant.name)}: "
            f"coeff={participant.coeff}, payment={escape_html(participant.payment)}"
        )
    return "<br>".join(lines)


def input_coeff_text_factory(data: StageData) -> str:
    participant_id = data.pending_payload.get("participant_id")
    if not participant_id or not data.party:
        return "Введите коэффициент"

    participant = data.party.get_participant(int(participant_id))
    return f"Введите коэффициент для {escape_html(participant.name)}"


def input_payment_text_factory(data: StageData) -> str:
    participant_id = data.pending_payload.get("participant_id")
    if not participant_id or not data.party:
        return "Введите сумму платежа"

    participant = data.party.get_participant(int(participant_id))
    return f"Введите сумму платежа для {escape_html(participant.name)}"
