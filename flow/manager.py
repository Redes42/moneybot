import logging
from telebot import types, TeleBot

from bot.log import log
from bot.safe_sender import send_safe_message
from flow.callback_codec import CallbackCodec
from db.app import Users, Persons
from entities.party import Party
from flow.menu import Menu
from flow.session import UserSession
from flow.stage_data import StageData
from flow.stages import InputStage, SelectStage, Stage, Stages
from logic.stage_logic import PreprocessResult


class FlowManager:
    def __init__(self, bot: TeleBot, menu: Menu):
        self.bot = bot
        self.menu = menu
        self.sessions = dict()

    def is_allowed_user(self, chat_id: int) -> bool:
        user_db = Users.get_user(chat_id)
        if user_db is None:
            return False
        return True

    def get_session(self, chat_id: int):
        if chat_id not in self.sessions:
            self.sessions[chat_id] = UserSession(
                chat_id=chat_id,
                current_stage=self.menu.start_stage,
                party=Party(),
                people=list(Persons.get_persons(chat_id))
            )
        return self.sessions[chat_id]

    def _make_stage_data(self, session: UserSession) -> StageData:
        return StageData(
            chat_id=session.chat_id,
            people=session.people,
            party=session.party,
            payload=session.payload,
        )

    def open_stage(self, session: UserSession, stage: Stage) -> None:
        previous_session = session.current_stage
        session.current_stage = stage
        stage_data = self._make_stage_data(session)
        log(logging.INFO, stage_data, previous_session, f'Opening stage {stage.name}')
        result: PreprocessResult = stage.preprocess(stage_data)
        if not result.skip_current_stage:
            prompt_data = self._make_stage_data(session)
            stage.render_message(prompt_data)

        else:
            self.open_stage(session, session.current_stage.default_child)


    def handle_callback(self, chat_id: int, callback_data: str) -> None:
        back = False
        session = self.get_session(chat_id)
        current_stage = session.current_stage
        if not isinstance(current_stage, SelectStage):
            return
        data = self._make_stage_data(session)
        stage = self.menu.get_stage_by_name(callback_data)
        if stage is None:
            payload = CallbackCodec.decode_payload(callback_data)
            data.payload.update(payload)
        else:
            if current_stage.parent:
                if current_stage.parent.name == stage.name:
                    back = True
        if not back:
            success = current_stage.process(data)
            if not success:
                return
            if current_stage.clear_payload_on_success:
                data.payload.clear()
        if stage is not None:
            self.open_stage(session, stage)
        else:
            self.open_stage(session, current_stage.default_child)

    def handle_message(self, message: types.Message) -> None:
        chat_id = message.chat.id
        text = message.text
        session = self.get_session(chat_id)
        current_stage = session.current_stage
        if not isinstance(current_stage, InputStage):
            stage_text = (
                f'Вы сейчас находитесь на этапе "{current_stage.text}".\n'
                f'Воспользуйтесь инструкциями, полученными выше'
            )
            send_safe_message(
                chat_id,
                f'Неизвестное сообщение.\n{stage_text}'
            )
            return
        session.payload['value'] = text
        data = self._make_stage_data(session)
        success = current_stage.process(data)
        if not success:
            return
        if current_stage.clear_payload_on_success:
            data.payload.clear()
        if current_stage.children:
            self.open_stage(session, current_stage.default_child)
